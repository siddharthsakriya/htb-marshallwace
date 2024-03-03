const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'me',
  brokers: ['0.0.0.0:9093'],
});

const consumer = kafka.consumer({ groupId: 'test-group' });
let recentStockValues = [];
let messageCounter = 0;

async function startConsumer() {
  try {
    await consumer.connect();
    await consumer.subscribe({ topic: 'stock_data', fromBeginning: true });

    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const data = JSON.parse(message.value.toString());

        const transformedData = {
            x: messageCounter++, 
            y: data.price,
        };

        recentStockValues.push(transformedData);
        
        if (recentStockValues.length > 14) {
            recentStockValues.shift(); 
        }

        for (let i = 0; i < recentStockValues.length; i++) {
            recentStockValues[i].x = i;
        }


        console.log(recentStockValues);
      },
    });
  } catch (error) {
    console.error("Error in consumer:", error);
  }
}
function getRecentStockValues() {
  return recentStockValues;
}

startConsumer().catch(console.error);
module.exports = {
  getRecentStockValues,
  startConsumer,
};


// startConsumer();