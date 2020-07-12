const AWS = require('aws-sdk');

const dynamo = new AWS.DynamoDB.DocumentClient();


exports.handler = async (event) => {
    console.log('Received event:', JSON.stringify(event, null, 2));

    const payload = {
        TableName: 'HadithCorrections',
        Item: JSON.parse(event.body)
    };
    
    return await dynamo.put(payload).promise();
};
