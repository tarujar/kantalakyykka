# Scripts

## Create types for frontend

`npx openapi-typescript-codegen --input http://localhost:8000/openapi.json --output ./frontend/src/types/`

Or if types are mismatching in data. Do fix the types defined in backend code and run the script after that.

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
