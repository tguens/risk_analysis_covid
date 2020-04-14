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
- Republique Democratique Congo
- Congo Brazzaville
- Burkina Faso
- Burundi
- Comores
- Gabon
- Madagascar
- Mauritanie
- Togo
- Centrafrique
"""

sources_algeria = []


sources_senegal = ["LeSoleilonline", "QuotidienSN"]
sources_gabon = ["InfosGabon"]
sources_mali = ["JourDuMali"]
sources_rdc = ["CongoActu"]

#sources_senegal = ["QuotidienSN"]

sources = {'Senegal': sources_senegal,
           'Algeria': sources_algeria, 
           'Mali':sources_mali, 
           'Gabon': sources_gabon, 
           'RDC':sources_rdc}

header = ['id',
          'title',
          'text',
          'Date',
          'country',
          'source',
          'tweet']
