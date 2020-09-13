aws dynamodb create-table --table-name HadithCorrections \
   --attribute-definitions AttributeName=id,AttributeType=S \
   --key-schema AttributeName=id,KeyType=HASH \
   --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
   --endpoint-url http://dynamodb-local:8000 --region us-west-2

aws dynamodb create-table --table-name HadithCorrectionsArchive \
   --attribute-definitions AttributeName=urn,AttributeType=S AttributeName=id,AttributeType=S \
   --key-schema AttributeName=urn,KeyType=HASH AttributeName=id,KeyType=RANGE \
   --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
   --endpoint-url http://dynamodb-local:8000 --region us-west-2

aws dynamodb put-item --table-name HadithCorrections --item '{
   "id":{
      "S":"123"
   },
   "urn":{
      "S":"10"
   },
   "attr":{
      "S":"body"
   },
   "val":{
      "S":"<p>Narrated Umar bin Al-Khattab:</p><p>I heard Allah''s Messenger (ﷺ) saying, \"The reward of deeds depends upon the  intentions and every person will get the reward according to what he has intended. So whoever emigrated for worldly benefits or for a woman to marry, his emigration was for what he emigrated for.\"</p>"
   },
   "lang": {
      "S": "en"
   },
   "queue": {
      "S": "global"
   },
   "comment":{
      "S":"Fixed formatting"
   },
   "submittedBy":{
      "S":"someone@example.com"
   }
}' --endpoint-url http://dynamodb-local:8000 --region us-west-2

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
}' --endpoint-url http://dynamodb-local:8000 --region us-west-2