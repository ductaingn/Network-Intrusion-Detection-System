import { Kafka } from 'kafkajs';
// import WebSocket from 'ws';
import { WebSocketServer } from 'ws';
import config from '../config.js';

const kafka = new Kafka({
  clientId: 'websocket-kafka-consumer',
  brokers: [config.kafkaBroker]
});

const consumer = kafka.consumer({ groupId: 'websocket-group' });

async function runKafkaConsumer() {
  await consumer.connect();
  await consumer.subscribe({ topic: 'testOutput', fromBeginning: true });

  consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const key = message.key ? message.key.toString() : null;
      const value = message.value ? message.value.toString() : null;

      // console.log(`Received message: ${key}: ${value}`);

      broadcastToClients({ key, value });
    }
  });
}

const wss = new WebSocketServer({ port: 8080 });

let clients = [];

wss.on('connection', (ws) => {
  console.log('New WebSocket connection');
  clients.push(ws);

  ws.on('message', (message) => {
    console.log(`Received from client: ${message}`);
  });

  ws.on('close', () => {
    clients = clients.filter(client => client !== ws);
  });
});


function broadcastToClients(data) {
  clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(data));
    }
  });
}


runKafkaConsumer().catch(console.error);