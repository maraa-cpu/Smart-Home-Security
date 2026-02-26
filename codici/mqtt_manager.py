from umqttsimple import MQTTClient
import machine
import time
import config

class MQTTManager:
    def __init__(self):
        self.broker = config.MQTT_BROKER
        self.topic_sub = config.MQTT_TOPIC_SUB
        self.topic_pub = config.MQTT_TOPIC_PUB
        self.cmd_received = None
        
        self.client = MQTTClient(
            config.MQTT_CLIENT_ID, 
            config.MQTT_BROKER, 
            port=config.MQTT_PORT, 
            user=config.MQTT_USER, 
            password=config.MQTT_PASSWORD
        )
        self.client.set_callback(self._callback)

    def _callback(self, topic, msg):
        print(f"MQTT MSG: {topic} -> {msg}")
        try:
            decoded = msg.decode().strip().upper()
            self.cmd_received = decoded
        except:
            pass

    def connect(self):
        try:
            self.client.connect()
            if self.topic_sub:
                self.client.subscribe(self.topic_sub)
            return True
        except Exception as e:
            return False

    def check_msg(self):
        try:
            self.client.check_msg()
        except OSError:
            try:
                self.connect()
            except:
                pass

    def publish(self, msg):
        if self.topic_pub:
            try:
                self.client.publish(self.topic_pub, msg)
            except Exception as e:
                print(f"MQTT Publish Error: {e}")
                try:
                    self.connect()
                    self.client.publish(self.topic_pub, msg)
                except Exception as e2:
                    print(f"Retry Publish Error: {e2}")

    def get_last_command(self):
        cmd = self.cmd_received
        self.cmd_received = None
        return cmd


