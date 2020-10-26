aws dynamodb create-table --table-name HadithCorrections \
   --attribute-definitions AttributeName=queue,AttributeType=S AttributeName=id,AttributeType=S \
   --key-schema AttributeName=queue,KeyType=HASH AttributeName=id,KeyType=RANGE \
   --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
   --endpoint-url http://dynamodb-local:8000 --region us-west-2

aws dynamodb create-table --table-name HadithCorrectionsArchive \
   --attribute-definitions AttributeName=urn,AttributeType=S AttributeName=id,AttributeType=S \
   --key-schema AttributeName=urn,KeyType=HASH AttributeName=id,KeyType=RANGE \
   --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
   --endpoint-url http://dynamodb-local:8000 --region us-west-2

aws dynamodb create-table --table-name Users \
   --attribute-definitions AttributeName=username,AttributeType=S \
   --key-schema AttributeName=username,KeyType=HASH \
   --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
   --endpoint-url http://dynamodb-local:8000 --region us-west-2

for i in {1..10}
do
   ID=`date +%s`
   aws dynamodb put-item --table-name HadithCorrections --item '{
      "queue":{
         "S":"global"
      },
      "id":{
         "S":"'"$ID:abcdef$i"'"
      },
      "urn":{
         "S":"10"
      },
      "attr":{
         "S":"body"
      },
      "val":{
         "S":"'"$i"' Narrated Umar bin Al-Khattab:<p>I heard Allah''s Messenger (ﷺ) saying, \"The reward of deeds depends upon the  intentions and every person will get the reward according to what he has intended. So whoever emigrated for worldly benefits or for a woman to marry, his emigration was for what he emigrated for.\"</p>"
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
      },
      "version": {
         "N": "0"
      }
   }' --endpoint-url http://dynamodb-local:8000 --region us-west-2
done

aws dynamodb put-item --table-name HadithCorrectionsArchive --item '{
   "queue":{
      "S":"global"
   },
   "id":{
      "S":"1234:ghijk99"
   },
   "urn":{
      "S":"50"
   },
   "attr":{
      "S":"body"
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
   },
   "version": {
      "N": "1"
   }
}' --endpoint-url http://dynamodb-local:8000 --region us-west-2

aws dynamodb put-item --table-name Users --item '{
    "username":{
        "S": "guest"
    },
    "permissions":{
        "M":{
              "manage_users": {
                "BOOL": true
              },
              "queues":{
                "SS": ["global", "secondary"]
              }
        }
    }
}' --endpoint-url http://dynamodb-local:8000 --region us-west-2
