# Scripts

## Startup script

### database

`sh start_database.sh``

### app startup

`sh startup.sh`

make sure the migrations are executable
`chmod +x startup.sh`

## Create types for frontend

`npm run openapi-ts  ./frontend/src/openapi/`

Or if types are mismatching in data. Do fix the types defined in backend code and run the script after that.

## Schemas swagger

You can see the schemas running from `http://localhost:8000/docs/`
You can see the admin panel from `http://localhost:8000/admin/`

## Kyykän pelisanasto

### Perustermit

| Englanti | Suomi   | Selitys                                                    |
| -------- | ------- | ---------------------------------------------------------- |
| game     | peli    | Kokonainen ottelu, sisältää kaksi erää                     |
| set      | erä     | Pelin puolikas, jossa kumpikin joukkue heittää vuorollaan  |
| throw    | heitto  | Yksittäinen heitto erän aikana                             |
| round    | kierros | Yksi heittokierros, jossa kaikki pelaajat heittävät kerran |

### Erikoistermit

| Termi | Selitys by AI                                     |
| ----- | ------------------------------------------------- |
| pappi | Pystyyn jäänyt kyykkä, -1 piste                   |
| hauki | Kyykän heitto matalalla lentoradalla ("hauki ui") |
| akka  | Kyykän heitto korkealla kaarella ("akka lentää")  |

### Pelin rakenne
