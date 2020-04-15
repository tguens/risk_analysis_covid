"""
Useful link: 
http://www.africain.info/afrique-tous-les-journaux-africains


William :
-#Cote d’ivoire
-#Cameroun
-#Algerie
-#Benin
-Djibouti
-#Guinée
-#Ile Maurice
-#Niger
-Tanzanie ???
-Tunisie
-Maroc


Theo :
- Mali
- Senegal
- Gabon
- Republique Democratique Congo
- Burkina Faso
- Togo
- Burundi

- Comores
- Madagascar

- Mauritanie
- Centrafrique
- Congo Brazzaville
"""
#William
sources_algeria = ["elwatancom","ObservAlgerie"]
sources_ivory_coast = ["Koaci","Linfodrome"]
sources_cameroun=["actucameroun","cameroun24"]
sources_benin=["24haubenin","MatinLibre"]
sources_djibouti=[]# La voix de Djibouti mais aucun article sur leur twitter
sources_guinea=["Africaguinee","VisionGuinee"]
source_maurice = ["lemauricien_com","defimediainfo"]
sources_niger =["actuniger","nigerexpress"]
sources_tunisia=["tunistribune","nawaat"]
sources_maroc=["Leconomiste_","lanouvelleT","LiberationMaroc"]

#Theo
sources_senegal = ["LeSoleilonline", "QuotidienSN"]
sources_gabon = ["InfosGabon"]
sources_mali = ["JourDuMali"]
sources_rdc = ["CongoActu"]
sources_burkina = ["Lefaso_net"]
sources_togo = ["SAVOIRNEWS1"]
sources_burundi = ["iwacuinfo"]
sources_comores = ["comoresinfos"]
sources_madagascar = ["madatribune"]

#sources_senegal = ["QuotidienSN"]

            
sources = {'Algeria': sources_algeria,
           'Ivory Coast':sources_ivory_coast,
           'Cameroun':sources_cameroun,
           'Benin':sources_benin,
           'Guinee':sources_guinea,
           "Ile Maurice":source_maurice,
           "Niger":sources_niger,
           "Tunisia":sources_tunisia,
           "Maroc":sources_maroc,
           'Senegal': sources_senegal,
           'Mali':sources_mali, 
           'Gabon': sources_gabon, 
           'RDC':sources_rdc, 
           'Burkina':sources_burkina, 
           'Togo':sources_togo,
           'Burundi':sources_burundi, 
           'Comores':sources_comores, 
           'Madagascar':sources_madagascar}


header = ['id',
          'title',
          'text',
          'Date',
          'country',
          'source',
          'tweet']
