import pandas as pd
import numpy as np
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import requests

headers = {'User-Agent': 'XY'}

##Map Vessel_type
map_vt_url="https://www.gabrielfuentes.org/tables_emissions/map_vessel_type_imo4.json"
map_vessel_type = requests.get(url=map_vt_url, headers=headers).content
map_vessel_type=pd.read_json(map_vessel_type)

#Types Table
vt_url="https://www.gabrielfuentes.org/tables_emissions/type_table.json"
vessel_type = requests.get(url=vt_url, headers=headers).content
vessel_type=pd.read_json(vessel_type)

#####Functions--------------------
##Cleaning punctuations from new ais_types
def clean_string(text):
    text=''.join([word for word in text if word not in string.punctuation])
    text=text.lower()
    return text

##base shiptypelevel5 to comapre to
base_stype=map_vessel_type.ShiptypeLevel5.unique().tolist()

##Compare similiraty higher than 50% and return respective shiptype5 value
def compare_similarity(text):
    comp=[text]+base_stype
    cleaned=list(map(clean_string,comp))
    vectors=CountVectorizer().fit_transform(cleaned)
    vectors=vectors.toarray()
    csim=cosine_similarity(vectors)
    
    val_com=np.max(csim[0,1:])
    
    if val_com>0.75:
        v_type=base_stype[np.argmax(csim[0,1:])]
    else:
        v_type=None
    
    return v_type   

##Imo bin finder
def bin_finder(vessel_t,value,df_in):
    try:
        bin_imo=df_in[((df_in.StandardVesselType==vessel_t)&(df_in.mindiff<=value)&(df_in.maxdiff>=value))].imo4bin.iloc[0]
    except:
        bin_imo=0
    return bin_imo
###++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
###Unit of cargo measurement per vessel type
unit={'Bulk carrier':'Deadweight',
     'Chemical tanker':'Deadweight',
     'Container':"TEU",
     'General cargo':'Deadweight',
     'Liquified gas tanker':'GrossTonnage',
     'Oil tanker':'Deadweight',
     'Other liquids tankers':'Deadweight',
     'Ferry-pax only':'GrossTonnage',
     'Cruise':'GrossTonnage',
     'Ferry-RoPax':'GrossTonnage',
     'Refrigerated bulk':'Deadweight',
     'Ro-Ro':'Deadweight',
     'Vehicle':'GrossTonnage',
     'Yacht':'GrossTonnage',
     'Service-tug':'GrossTonnage',
     'Miscellaneous-fishing':'GrossTonnage',
     'Offshore':'GrossTonnage',
     'Service-other':'GrossTonnage',
     'Miscellaneous-other':'GrossTonnage'}

##Engine type allocation
oil_eng=['Diesel-Elec & Gas Turbine(s)','Oil Engs & Fuel Cell-Electric''Oil Eng(s), Elec-Dr, Aux Sail','Oil Engines, Geared & Elec. Dr','Oil Eng(s) & Gas Turb(s) El.Dr','Oil Eng(s) Direct Dr, Aux Sail','Oil Eng(s) Dd & Gas Turb(s) El','Oil Engines, F&S, Geared Drive','Oil Engines, Direct & Elec. Dr','Oil Engines, Elec. & Direct Dr','Oil Engine(s), Drive Unknown','Oil Engines, Elec. & Geared Dr','Oil Eng(s), Geared, Aux Sail','Oil Engs & Gas Turb(s), Geared','Oil Engine(s), Electric Drive','Oil Engine(s), Direct Drive','Oil Engine(s), Geared Drive']
sail=['Sail, Aux Petrol Eng(s) D.Dr.','Sail, Aux Oil Eng(s), Elec Dr.','Sail, Aux Oil Eng(s), Geared','Sail','Sail, Aux Oil Eng(s) Direct-Dr',]
gas_tur=['Gas Turbine(s), Electric Drive','Gas Turbine(s) Or Diesel Elec.','Gas Turbine(s) & Diesel Elec.','Gas Turbine(s), Geared Drive',]
steam=['S.Turb, Gear & Oil Eng(s), Ele','St. Turb(s) Elec Dr. Or D.E.','Steam Turbine(s), Direct Drive','Steam Recip(s) With Lp Turbine','Steam Turbine(s), Elec.Drive','Steam- & Gas-Turbines, Geared','Steam Turbine(s), Geared Drive','Steam Recip(s), Direct Drive',]


def adapted_specs_imo(df_unique_imo,specs):
    """Input (IMPORTANT): AIS Df with unique IMO. IF no IMO then unique MMSI; DF Specs.
    Rules adapted to IMO GHG 4 study. Important to merge with AIS sequences
    Output: Vessel Specs of vessels in AIS records with appropiate IMO GHG4 categories"""
    
    df_unique_imo.rename(columns={"vessel_type_main":"ais_type","length":"ais_loa","width":"ais_beam"},inplace=True)
    ind=df_unique_imo[["imo","mmsi","ais_type","ais_loa","ais_beam"]]
    ind=pd.merge(ind,specs,how="left",left_on="imo",right_on="LRIMOShipNo")
    
    ##Records with no IMO number is checked by MMSI
    mmsi_p=ind[ind.LRIMOShipNo.isnull()][["imo","mmsi"]]
    mmsi_p=pd.merge(mmsi_p,specs,how="left",left_on="mmsi",right_on='MaritimeMobileServiceIdentityMMSINumber')
    
    imo_p=ind[ind.LRIMOShipNo.notnull()]
    
    ind=pd.concat([imo_p,mmsi_p])
    
    ind=ind.assign(ShiptypeLevel5=np.where(ind.ShiptypeLevel5.isnull(),ind.ais_type,ind.ShiptypeLevel5))
    ##Remove values with Shiptypelevel5 null. Not much else to do with this records. 
    ##Remove nans before similarity check
    ind=ind[ind.ShiptypeLevel5.notnull()]
    ind=ind.assign(ShiptypeLevel5=np.where(ind.ShiptypeLevel5.isin(base_stype),ind.ShiptypeLevel5,
                                          ind.ShiptypeLevel5.apply(lambda x: compare_similarity(x))))
    ##Ensure no vessel without Standard vessel type
    ind=ind[ind.ShiptypeLevel5.notnull()]

    ##---Pending----Inputation here input from AIS(Length,Beam) and Shiptypelevel5 to have [DWT,GT]. Potential RF Regressor (missForest).
    
    ind=pd.merge(ind,map_vessel_type,how="left",on='ShiptypeLevel5')
    
    ind=ind.assign(imobin=ind.apply(lambda x: bin_finder(x.StandardVesselType,x[unit[x.StandardVesselType]],vessel_type),axis=1))
    
    ###Fuel allocation
    ind=ind.assign(fuel=np.where(((ind.FuelType1First=='Residual Fuel')|(ind.FuelType2Second=='Residual Fuel')),
                                 np.where(((ind.PropulsionType.isin(['Steam Turbine(s), Geared Drive','S.Turb, Gear & Oil Eng(s), Ele','Steam Recip(s), Direct Drive','Steam- & Gas-Turbines, Geared','Steam Turbine(s), Elec.Drive','Steam Recip(s) With Lp Turbine','Steam Turbine(s), Direct Drive','St. Turb(s) Elec Dr. Or D.E.',]))\
                                                                  &(ind.StandardVesselType=='Liquified gas tanker')),"LNG","HFO"),
                                     np.where(((ind.FuelType1First=='Distillate Fuel')&(ind.FuelType2Second=='Distillate Fuel')),"MDO",
                                     np.where(((ind.FuelType1First=='Distillate Fuel')&(ind.FuelType2Second.isin(['Yes, But Type Not Known','Not Applicable','Unknown',None]))),"MDO",
                                     np.where(((ind.FuelType1First.isin(['Yes, But Type Not Known','Not Applicable','Unknown',None]))&(ind.FuelType2Second=='Distillate Fuel')),"MDO",
                                     np.where(((ind.FuelType1First=='Coal')&(ind.FuelType2Second=='Distillate Fuel')),"MDO",
                                     np.where(((ind.FuelType1First=='Methanol')&(ind.FuelType2Second=='Distillate Fuel')),'Methanol',
                                         np.where((((ind.FuelType1First=='Residual Fuel')|(ind.FuelType2Second=='Residual Fuel'))&\
                                                   ((ind.StandardVesselType=='Liquified gas tanker')&(ind.PropulsionType.isin(['Steam Turbine(s), Geared Drive','S.Turb, Gear & Oil Eng(s), Ele','Steam Recip(s), Direct Drive','Steam- & Gas-Turbines, Geared','Steam Turbine(s), Elec.Drive','Steam Recip(s) With Lp Turbine','Steam Turbine(s), Direct Drive','St. Turb(s) Elec Dr. Or D.E.',])))),'LNG',
                                         np.where(((ind.FuelType1First=='Gas Boil Off')&(ind.FuelType2Second=='Distillate Fuel')),'LNG',
                                         np.where(((ind.FuelType1First.isin(["LNG",'Lpg','Lng']))&(ind.FuelType2Second=='Distillate Fuel')),'LNG',
                                         np.where(((ind.FuelType1First.isin(["LNG",'Lpg','Lng']))&(ind.FuelType2Second.isin(['Yes, But Type Not Known','Not Applicable','Unknown',None]))),'LNG',
                                         np.where(((ind.FuelType1First.isin(['Yes, But Type Not Known','Not Applicable','Unknown',None]))&(ind.FuelType2Second.isin(["LNG",'Lpg','Lng']))),'LNG',      
                                         np.where(ind.FuelType2Second=='Gas Boil Off','LNG',
                                             np.where(((ind.FuelType1First=='Nuclear')&(ind.FuelType2Second=='Distillate Fuel')),'Nuclear',
                                             np.where(((ind.FuelType1First=='Nuclear')&(ind.FuelType2Second.isin(['Yes, But Type Not Known','Not Applicable','Unknown',None]))),'Nuclear',
                                                      np.where(((ind.FuelType1First=='Coal')&(ind.FuelType2Second.isin(['Yes, But Type Not Known','Not Applicable','Unknown',None]))),'Coal',
                                                               np.where(ind.FuelType1First=='Methanol','Methanol',                                              
                                 None))))))))))))))))
                  )


    ###Engine types
    ind=ind.assign(meType=np.where(ind.PropulsionType.isin(oil_eng),
                                  np.where(ind.MainEngineRPM<=300,"SSD",
                                  np.where(ind.MainEngineRPM.between(301,900),"MSD",
                                  np.where(ind.MainEngineRPM>900,"HSD","SSD"))),
                           np.where(ind.PropulsionType.isin(['Petrol Engine(s), Direct Drive','Petrol Engine(s), Geared Drive']),"HSD",
                           np.where(ind.fuel=="LNG",
                                   np.where(((ind.MainEngineModel.str.contains("X"))|(ind.MainEngineModel.str.contains("DF"))),"LNG-Otto-SS",
                                   np.where(ind.MainEngineRPM>300,"LNG-Otto-MS",    
                                   np.where(ind.MainEngineModel.str.contains("ME"),"LNG-Diesel","LNG-Otto-MS"                                       
                                   ))), 
                           np.where(ind.fuel=="Methanol","Methanol",         
                           np.where(ind.PropulsionType.isin(sail),"Sail",
                           np.where(ind.PropulsionType=='Battery-Electric',"Batteries",
                           np.where(ind.PropulsionType=='Non-Propelled','Non-Propelled', 
                           "SSD"))))))))
    ##Gas turbines and Steam turbines conditional on former filters
    ind=ind.assign(meType=np.where(((ind.PropulsionType.isin(gas_tur))|(((ind.meType.isin(["SSD","MSD"]))&(ind.fuel=="LNG")))),"Gas Turbine",
                          np.where(ind.PropulsionType.isin(steam),"Steam Turbine",
                          ind.meType                      
                      ))
                  )
    ind=ind.assign(fuel=np.where(ind.meType=="Sail","Sail",
                        np.where(ind.meType=="Non-Propelled","Non-Propelled",
                        np.where(((ind.fuel.isnull())&(ind.meType=="HSD")),"MDO",
                        np.where(((ind.fuel.isnull())&(ind.meType=="MSD")),"MDO",
                        np.where(((ind.fuel.isnull())&(ind.meType=="SSD")),"HFO",
                                ind.fuel)))))
                  )
    
    ind=ind[['imo','mmsi','LRIMOShipNo', 'MaritimeMobileServiceIdentityMMSINumber', 'GrossTonnage', 'Deadweight', 'LengthOverallLOA',
     'DateOfBuild', 'TEU', 'Powerkwmax', 'MainEngineModel', 'Speed', 'Speedmax', 'Speedservice', 'BreadthExtreme', 'Draught', 'FuelType1Capacity',
     'FuelType2Capacity', 'LightDisplacementTonnage', 'MainEngineRPM', 'MainEngineType', 'Powerkwservice', 'PropulsionType',
     'ShiptypeLevel5', 'TotalBunkerCapacity', 'StandardVesselType', 'imobin', 'fuel', 'meType']]
    
    return ind
