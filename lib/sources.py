"""
Useful link: 
http://www.africain.info/afrique-tous-les-journaux-africains


William :
-Cote d’ivoire
-Cameroun
-Algerie
-Benin
-Djibouti
-Guinée
-Guinée équatoriale ???
-Niger
-Rwanda ???
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
- Congo Brazzaville
- Centrafrique

- Mauritanie


"""

sources_algeria = []


sources_senegal = ["LeSoleilonline", 
                    "QuotidienSN"]
sources_gabon = ["InfosGabon"]
sources_mali = ["JourDuMali"]
sources_rdc = ["CongoActu"]
sources_burkina = ["Lefaso_net"]
sources_togo = ["SAVOIRNEWS1"]
sources_burundi = ["iwacuinfo"]
sources_comores = ["comoresinfos"]
sources_madagascar = ["madatribune"]
sources_congo = ["ICIBrazza"]
sources_centrafrique = ["CorbeauNews"]

#sources_senegal = ["QuotidienSN"]

sources = {'Senegal': sources_senegal,
           'Algeria': sources_algeria, 
           'Mali':sources_mali, 
           'Gabon': sources_gabon, 
           'RDC':sources_rdc, 
           'Burkina':sources_burkina, 
           'Togo':sources_togo,
           'Burundi':sources_burundi, 
           'Comores':sources_comores, 
           'Madagascar':sources_madagascar, 
           'Congo':sources_congo, 
           'Centrafrique':sources_centrafrique}

header = ['id',
          'title',
          'text',
          'Date',
          'country',
          'source',
          'tweet']
