# Data Engineering

The exercise is to develop a distributed Extract-Transform-Load (ETL) application.

The pipeline has two parts:
1. A producer: generates mock data and sends it to a Kafka topic called `prices`
1. A consumer: reads the data from the `prices` topic and calculates some statistics. 

The consumer application reads data from a kafka topic and computes some statistics and prints them to standard output for visual inspection.

The application is run using python.
The image used to deploy kafka can be found [here](https://hub.docker.com/r/landoop/fast-data-dev/dockerfile)
Further information can be found on the [github](https://github.com/lensesio/fast-data-dev)


# Requirements
- docker-compose version 1.25.4+
- docker 18.09.6+

# Producer
This application writes data to a `prices` Kafka topic.

A template for the producer is in the [producer](./producer/producer.py). Data, in json format, should be written to the `prices` topic.

Each message includes three pieces of data:
1. ts: the event timestamp (yyyy-mm-dd hh:mm:ss.fff)
2. symbol: a stock symbol, randomly selected from a pre-defined list of 5 symbols.
3. price: a float with two-digit precision.

Sample message
```
{
    "ts": "2021-03-10 16:21:32.000", 
    "symbol": "APPL", 
    "price": 238.32
}
```

The producer should send 5000 messages to the topic and exit. To ensure that we have some results in step 3 of the cosumer you can use `random.normalvariate` to generate the prices with a normal distribution.

The borker url is `kafka:9092` and the topic name is `prices`.

# Consumer
The consumer is an application that reads all data available in the `prices` topic and peforms the following computations: 

1. Count and print the number of messages in the topic.
   
2. Calculate the min, max, mean and standard deviation for the prices per symbol and print to screen.  
 
3. Find any outliers using the computed statistics from step 2, print only the timestamp, symbol and anomalous price.  

The consumer uses pyspark to process the data and print the statistics computed from the messages.

# UI
To view the prices topic and navigate through the messages interactively, visit http://localhost:3030.

# Useful docker-compose commands

### Run all services
Use this command to run all services. The producer application should execute and send messges to the `prices` topic. The consumer application should read the data and print the output to screen.

```
docker-compose up --remove-orphans --force-recreate --build
```
--- 


### Producer
```
docker-compose up --remove-orphans --force-recreate --build producer
```
---

### Consumer
```
docker-compose up --remove-orphans --force-recreate --build consumer
```
---

### Stop all services
```
docker-compose down
```
--- 

### Considerations

- When producing the messages, double the number of messages get sent than are generated from the generator function in producer.py. This is an interesting error that has not yet been removed but for the purposes of this assignment I have generate half the prices to compensate. With more time I would investigate this further.

- Have yet to implement sophisticated tests to ensure maintainability.

