// jshint ignore: start
'use strict';
var aws = require('aws-sdk');
var doc;

module.exports = (function() {
    return {
        get: function(table, userId, callback, endpoint_url) {
            if(!table) {
                callback('DynamoDB Table name is not set.', null);
            }

            if(!doc) {
                if (endpoint_url) {
                    // not sure how to control this, but the local dynamodb seems to set region to east
                    doc = new aws.DynamoDB.DocumentClient({apiVersion: '2012-08-10', region: 'us-east-1', endpoint: endpoint_url});
                }
                else {
                    doc = new aws.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
                }
            }

            var params = {
                Key: {
                    userId: userId
                },
                TableName: table,
                ConsistentRead: true
            };

            doc.get(params, function(err, data){
                if(err) {
                    console.log('get error: ' + JSON.stringify(err, null, 4));

                    if(err.code === 'ResourceNotFoundException') {
                        let dynamoClient = undefined;
                        if (endpoint_url) {
                          dynamoClient = new aws.DynamoDB({region: "us-east-1", endpoint: endpoint_url});
                        }
                        else {
                          dynamoClient = new aws.DynamoDB();
                        }
                        newTableParams['TableName'] = table;
                        dynamoClient.createTable(newTableParams, function (err, data) {
                            if(err) {
                                console.log('Error creating table: ' + JSON.stringify(err, null, 4));
                            }
                            console.log('Creating table ' + table + ':\n' + JSON.stringify(data));
                            callback(err, {});
                        });
                    } else {
                        callback(err, null);
                    }
                } else {
                    if(isEmptyObject(data)) {
                        callback(null, {});
                    } else {
                        callback(null, data.Item['mapAttr']);
                    }
                }
            });
        },

        set: function(table, userId, data, callback) {
            if(!table) {
                callback('DynamoDB Table name is not set.', null);
            }

            if(!doc) {
                if (endpoint_url) {
                    doc = new aws.DynamoDB.DocumentClient({apiVersion: '2012-08-10', region: 'us-east-1', endpoint: endpoint_url});
                }
                else {
                    doc = new aws.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
                }
            }

            var params = {
                Item: {
                    userId: userId,
                    mapAttr: data
                },
                TableName: table
            };

            doc.put(params, function(err, data) {
                if(err) {
                    console.log('Error during DynamoDB put:' + err);
                }
                callback(err, data);
            });
        }
    };
})();

function isEmptyObject(obj) {
    return !Object.keys(obj).length;
}

var newTableParams = {
    AttributeDefinitions: [
        {
            AttributeName: 'userId',
            AttributeType: 'S'
        }
    ],
    KeySchema: [
        {
            AttributeName: 'userId',
            KeyType: 'HASH'
        }
    ],
    ProvisionedThroughput: {
        ReadCapacityUnits: 1,
        WriteCapacityUnits: 1
    }
};
