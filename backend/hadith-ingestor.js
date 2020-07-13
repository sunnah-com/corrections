const AWS = require('aws-sdk');

const dynamo = new AWS.DynamoDB.DocumentClient();


exports.handler = async (event, context) => {
    console.log('Received event:', JSON.stringify(event, null, 2));

    const payload = {
        TableName: 'HadithCorrections',
        Item: JSON.parse(event.body)
    };

    payload.Item.id = context.awsRequestId;
    
    return await dynamo.put(payload).promise();
};
