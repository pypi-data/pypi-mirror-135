#Состав библиотеки
---------------------------------------------------------------------------------  
1. Класс Factory для получения экземпляров сервисов без указания путей к сервисам и секретов. Для работы нужно сконфигурировать переменные окружения VAULT_URL и VAULT_TOKEN, или явно передать url и token при создании экземпляра класса). Далее секреты автоматически достаются из vault, пути из consul
2. Декоратор @log(logger=you_logger)
3. Декоратор @retry(count=10, sleep=0.5)
## Установка
---------------------------------------------------------------------------------  
Requests is available on PyPI:\
$ python -m pip install dvgroup_factory\
from dvgroup_factory import factory

##Порядок работы:
---------------------------------------------------------------------------------  
1. Получить объект фабрики:
   1. fc = factory.Factory(vault_url=url, vault_token=token)
   2. 2.1 fc = factory.Factory(), если определены переменные окружения **VAULT_URL и VAULT_TOKEN**
2. Получить объект сервиса (в kwargs передаются параметры не связанные с url и secrets):
   1. ch_client = fc.clickhouse_client(secure=True, database="db1", verify=False)
   2. kafka_p = fc.kafka_producer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
3. По умолчанию, если ранее уже был создан объект сервиса, то при следующем запросе, будет возвращен ранее созданный.
4. Для получения нового объекта (если ранее уже был получен экземпляр), требуется переддать параметр new=True: 
   1. kafka_p2 = fc.kafka_producer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), ***new=True***)
5. Для получения именованного экземпляра требуется указать параметр ***instance_name***
   1. kafka_p2 = fc.kafka_producer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), ***instance_name="Name"***)
6. Для понимания, какие методы (классы сервисов) реализованы, следует вызвать метод info(), который возвратит след.информацию:

Создание экземпляра:\
---------------------------------------------------------------------------------   
    ins = Factory(vault_url=url, vault_token=token)\
Методы: \
   1 ins.vault_client(url: str, token: str)\
   2 ins.consul(**kwargs)\
   3 ins.kafka_producer(**kwargs)\
   4 ins.kafka_consumer(*topics,**kwargs)\
   3 ins.aiokafka_producer(**kwargs)\
   4 ins.aiokafka_consumer(*topics,**kwargs)\
   5 ins.clickhouse_client(**kwargs)\
   6 ins.azure_container_client(**kwargs)\
   7 ins.loki_handler(**kwargs)\
   8 ins.gp_connection()\ 
Для создания нового экземпляра укажите в kwargs: new=True\
Пути настроек в consul:\
   {"clickhouse": "env/databases/clickhouse", "kafka": "env/databases/kafka", "ms-azure-se": "env/databases/ms-azure-se", "loki": "env/databases/loki"}

#Пример кода:
----------------------------------------------------------------------------------
from dvgrop_factory import factory as fc

###Получаю экземпляр фабрики
factory = fc.Factory()

###Consul
consul = factory.consul()\
kafka_config = consul.kv["env/databases/kafka"]

###Clickhouse
ch = factory.clickhouse_client(database="db1", ca_certs="CA.pem")\
rs = ch.execute("SELECT COUNT(*) FROM db1.atol")

###KafkaProducer
k_p = factory.kafka_producer()

###KafkaConsumer
k_c = factory.kafka_consumer()

###azure.storage.blob.ContainerClient
a_cc = factory.azure_container_client(container_name="output")\
print(f'k_c = {a_cc}')

###azure.storage.blob.BlobCliennt
a_cc = factory.azure_blob_client(container_name="output", blob_name = "nm")

###logging_loki.LokiHandler
loki = factory.loki_handler(tags={"application": "atol-connector"}, version="1")\
loki.setLevel(logging.DEBUG)\
_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"\
loki.setFormatter(logging.Formatter(_log_format))\
logger = logging.getLogger('segments-api')\
logger.addHandler(loki)

###GreenPlum Connection
conn = factory.gp_connection()
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM raw_atol')
rs = cursor.fetchone()

###AIOKafka
async def aiostart():\
    consumer = factory.aiokafka_consumer("test-atol1", auto_offset_reset='earliest', enable_auto_commit=False, )\
    producer = factory.aiokafka_producer()\
    await consumer.start()\
    await producer.start()\
    try:\
        future = await producer.send("test-atol", value={"ASYNC": "start"})\
        #record_metadata = await future\
        key = None\
        async for msg in consumer:\
            print(f"async key {key} msg = {msg}")\
            msg.value["consumer-producer"] = True\
            msg.value["ASYNC"] = True\
            print(f"async msg = {msg}")\
            future = await producer.send("test-atol1", value=msg.value)\
    finally:\
        await consumer.stop()\
        await producer.stop()\

ioloop = asyncio.get_event_loop()\
tasks = [ioloop.create_task(aiostart())]\
ioloop.run_until_complete(asyncio.wait(tasks))\
ioloop.close()
