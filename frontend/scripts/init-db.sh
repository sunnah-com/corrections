aws dynamodb delete-table --table HadithCorrections \
   --endpoint-url http://localhost:8000 \
   --region localhost

aws dynamodb delete-table --table HadithCorrectionsArchive \
   --endpoint-url http://localhost:8000 \
   --region localhost

aws dynamodb create-table --table-name HadithCorrections \
   --attribute-definitions AttributeName=id,AttributeType=S \
   --key-schema AttributeName=id,KeyType=HASH \
   --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
   --endpoint-url http://localhost:8000 --region localhost

aws dynamodb create-table --table-name HadithCorrectionsArchive \
   --attribute-definitions AttributeName=urn,AttributeType=S AttributeName=id,AttributeType=S \
   --key-schema AttributeName=urn,KeyType=HASH AttributeName=id,KeyType=RANGE \
   --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
   --endpoint-url http://localhost:8000 --region localhost

aws dynamodb put-item --table-name HadithCorrections --item '{
   "id":{
      "S":"123"
   },
   "urn":{
      "S":"123"
   },
   "attr":{
      "S":"hadithText"
   },
   "val":{
      "S":"modifiedText"
   },
   "comment":{
      "S":"Spelling"
   },
   "submittedBy":{
      "S":"someone@example.com"
   }
}' --endpoint-url http://localhost:8000 --region localhost

aws dynamodb put-item --table-name HadithCorrectionsArchive --item '{
   "id":{
      "S":"1"
   },
   "urn":{
      "S":"50"
   },
   "attr":{
      "S":"hadithText"
   },
   "val":{
      "S":"modifiedText"
   },
   "comment":{
      "S":"Spelling"
   },
   "submittedBy":{
      "S":"someone@example.com"
   },
   "approved":{
      "BOOL":false
   },
   "moderatedOn":{
      "S":"2020-07-30 06:08:47"
   },
   "moderatedBy":{
      "S":"rootuser"
   }
}' --endpoint-url http://localhost:8000 --region localhost