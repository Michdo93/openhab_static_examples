import logging
import HABApp
from HABApp import Parameter
from HABApp.core.events import ValueChangeEvent, ValueUpdateEvent
from HABApp.openhab.events import ItemStateEvent
from HABApp.core.items import Item
from HABApp.openhab.items import OpenhabItem
from HABApp.openhab.items import ColorItem, ContactItem, DatetimeItem, DimmerItem, GroupItem, ImageItem, LocationItem, NumberItem, PlayerItem, RollershutterItem, StringItem, SwitchItem
import rospy
from openhab_msgs.msg import ColorState, ContactState, DateTimeState, DimmerState, GroupState, ImageState, LocationState, NumberState, PlayerState, RollershutterState, StringState, SwitchState
from openhab_msgs.msg import ColorCommand, ContactCommand, DateTimeCommand, DimmerCommand, ImageCommand, LocationCommand, NumberCommand, PlayerCommand, RollershutterCommand, StringCommand, SwitchCommand
from dateutil import parser
from datetime import datetime, timezone
import base64
import io
import cv2
from imageio import imread
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

log = logging.getLogger('openhab_bridge')
log_state = Parameter('openhab_bridge', 'log_state', default_value=True).value


class OpenHABBridge(HABApp.Rule):
    def __init__(self):
        super().__init__()

        for item in self.get_items(type=OpenhabItem):
            if type(item) is ColorItem:
                item.listen_event(self.ColorState, ItemStateEvent)
                rospy.Subscriber(
                    f'/openhab/items/{item.name}/command', ColorCommand, self.ColorCallback)
            elif type(item) is ContactItem:
                item.listen_event(self.ContactState, ItemStateEvent)
                rospy.Subscriber(
                    f'/openhab/items/{item.name}/command', ContactCommand, self.ContactCallback)
            elif type(item) is DatetimeItem:
                item.listen_event(self.DateTimeState, ItemStateEvent)
                rospy.Subscriber(
                    f'/openhab/items/{item.name}/command', DateTimeCommand, self.DateTimeCallback)
            elif type(item) is GroupItem:
                item.listen_event(self.GroupState, ItemStateEvent)
            elif type(item) is DimmerItem:
                item.listen_event(self.DimmerState, ItemStateEvent)
                rospy.Subscriber(
                    f'/openhab/items/{item.name}/command', DimmerCommand, self.DimmerCallback)
            elif type(item) is ImageItem:
                item.listen_event(self.ImageState, ItemStateEvent)
                rospy.Subscriber(
                    f'/openhab/items/{item.name}/command', ImageCommand, self.ImageCallback)
            elif type(item) is LocationItem:
                item.listen_event(self.LocationState, ItemStateEvent)
                rospy.Subscriber(
                    f'/openhab/items/{item.name}/command', LocationCommand, self.LocationCallback)
            elif type(item) is NumberItem:
                item.listen_event(self.NumberState, ItemStateEvent)
                rospy.Subscriber(
                    f'/openhab/items/{item.name}/command', NumberCommand, self.NumberCallback)
            elif type(item) is PlayerItem:
                item.listen_event(self.PlayerState, ItemStateEvent)
                rospy.Subscriber(
                    f'/openhab/items/{item.name}/command', PlayerCommand, self.PlayerCallback)
            elif type(item) is RollershutterItem:
                item.listen_event(self.RollershutterState, ItemStateEvent)
                rospy.Subscriber(
                    f'/openhab/items/{item.name}/command', RollershutterCommand, self.RollershutterCallback)
            elif type(item) is StringItem:
                item.listen_event(self.StringState, ItemStateEvent)
                rospy.Subscriber(
                    f'/openhab/items/{item.name}/command', StringCommand, self.StringCallback)
            elif type(item) is SwitchItem:
                item.listen_event(self.SwitchState, ItemStateEvent)
                rospy.Subscriber(
                    f'/openhab/items/{item.name}/command', SwitchCommand, self.SwitchCallback)

        rospy.spin()

    def ColorState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is ColorItem")
        msg = ColorState()
        msg.r = float(value[0])
        msg.g = float(value[1])
        msg.b = float(value[2])

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', ColorState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def ContactState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is ContactItem")
        msg = ContactState()
        if value == "OPEN":
            msg.state = ContactState.OPEN
        elif value == "CLOSED":
            msg.state = ContactState.CLOSED

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', ContactState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def DateTimeState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is DatetimeItem")
        msg = DateTimeState()
        msg.state = rospy.Time.from_sec(parser.parse(
            str(value)).replace(tzinfo=timezone.utc).timestamp())

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', DateTimeState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def DimmerState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is DimmerItem")
        msg = DimmerState()
        if 0 <= value <= 100:
            msg.state = int(value)

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', DimmerState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def GroupState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is GroupItem")
        msg = GroupState()

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', GroupState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def ImageState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is ImageItem")
        msg = ImageState()
        b64_bytes = base64.b64encode(value)
        b64_string = b64_bytes.decode()
        img = imread(io.BytesIO(base64.b64decode(b64_string)))
        cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        bridge = CvBridge()
        a = Image()
        a = bridge.cv2_to_imgmsg(
            cv2_img, encoding="passthrough")

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', ImageState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def LocationState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is LocationItem")
        msg = LocationState()
        splitted = value.split(",")
        msg.latitude = float(splitted[0])
        msg.longitude = float(splitted[1])
        msg.altitude = float(splitted[2])

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', LocationState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def NumberState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is NumberItem")
        msg = NumberState()
        msg.state = float(value)

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', NumberState, queue_size=1)

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', SwitchState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def PlayerState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is PlayerItem")
        msg = PlayerState()
        if value == "PLAY":
            msg.state = PlayerState.PLAY
        elif value == "PAUSE":
            msg.state = PlayerState.PAUSE
        elif value == "NEXT":
            msg.state = PlayerState.NEXT
        elif value == "PREVIOUS":
            msg.state = PlayerState.PREVIOUS
        elif value == "REWIND":
            msg.state = PlayerState.REWIND
        elif value == "FASTFORWARD":
            msg.state = PlayerState.FASTFORWARD

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', PlayerState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def RollershutterState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is RollershutterItem")
        msg = RollershutterState()
        if isinstance(value, int):
            msg.isstate = False
            msg.ispercentage = True

            if 0 <= value <= 100:
                msg.state = int(value)
        elif isinstance(value, str):
            msg.isstate = True
            msg.ispercentage = False

            if value == "UP":
                msg.state = RollershutterState.PLAY
            elif value == "DOWN":
                msg.state = RollershutterState.PAUSE
            elif value == "STOP":
                msg.state = RollershutterState.NEXT
            elif value == "MOVE":
                msg.state = RollershutterState.PREVIOUS

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', RollershutterState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def StringState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is StringItem")
        msg = StringState()
        msg.state = str(value)
        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', StringState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def SwitchState(self, event: ItemStateEvent):
        item = event.name
        value = event.value

        log.info("is SwitchItem")
        msg = SwitchState()
        if value == "ON":
            msg.state = SwitchState.ON
        elif value == "OFF":
            msg.state = SwitchState.OFF

        pub = rospy.Publisher(
            f'/openhab/items/{item}/state', SwitchState, queue_size=1)

        for my_item in self.get_items(name=item):
            item_type = my_item

        if hasattr(item_type, 'last_update'):
            msg.header.stamp = rospy.Time.from_sec(parser.parse(
                str(item_type.last_update)).replace(tzinfo=timezone.utc).timestamp())
        else:
            msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "/base_link"
        msg.item = str(item)

        log.info(
            f'Published ROS topic /openhab/items/{item}/state with {value}')

        rate = rospy.Rate(1)
        counter = 0

        while counter < 1:
            # wait for a connection to publisher
            # you can do whatever you like here or simply do nothing

            connections = pub.get_num_connections()
            if connections > 0:
                rospy.loginfo(
                    f'Published ROS topic /openhab/state/{item} with {value}')
                # pub.publish(msg)
                counter = counter + 1
            else:
                rate.sleep()

    def ColorCallback(self, data):
        item = data.item

        if data.iscommand == True:
            if data.command == ColorCommand.ON or data.command == ColorCommand.OFF or data.command == ColorCommand.INCREASE or data.command == ColorCommand.DECREASE:
                value = data.command
            else:
                value = None
        elif data.ispercentage == True:
            if 0 <= data.percentage <= 100:
                value = data.percentage
        elif data.ishsb == True:
            value = (data.hue, data.saturation, data.brightness)

        rospy.loginfo(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')
        log.info(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')

        self.oh.send_command(item, value)

    def ContactCallback(self, data):
        item = data.item

        if data.command == ContactCommand.OPEN or data.command == ContactCommand.CLOSED:
            value = data.command

        rospy.loginfo(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')
        log.info(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')

        self.oh.send_command(item, value)

    def DateTimeCallback(self, data):
        item = data.item
        value = datetime.utcfromtimestamp(
            data.command.to_sec()).strftime("%Y-%m-%dT%H:%M:%SZ")

        rospy.loginfo(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')
        log.info(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')

        self.oh.post_update(item, value)

    def DimmerCallback(self, data):
        item = data.item

        if data.iscommand == True:
            if data.command == DimmerCommand.ON or data.command == DimmerCommand.OFF or data.command == DimmerCommand.INCREASE or data.command == DimmerCommand.DECREASE:
                value = data.command
        elif data.ispercentage == True:
            if 0 <= data.percentage <= 100:
                value = data.percentage

        rospy.loginfo(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')
        log.info(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')

        self.oh.send_command(item, value)

    def ImageCallback(self, data):
        item = data.item

        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(
            data.command, desired_encoding='passthrough')

        retval, buffer = cv2.imencode('.jpg', cv_image)
        value = "data:image/jpg;base64" + \
            base64.b64encode(buffer).decode("utf-8")

        rospy.loginfo(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')
        log.info(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')

        self.oh.post_update(item, value)

    def LocationCallback(self, data):
        item = data.item

        value = str(data.latitude) + "," + \
            str(data.longitude) + "," + str(data.altitude)

        rospy.loginfo(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')
        log.info(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')

        self.oh.send_command(item, value)

    def NumberCallback(self, data):
        item = data.item

        if isinstance(data.number, float):
            value = data.command

        rospy.loginfo(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')
        log.info(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')

        self.oh.send_command(item, value)

    def PlayerCallback(self, data):
        item = data.item

        if data.command == PlayerCommand.PLAY or data.command == PlayerCommand.PAUSE or data.command == PlayerCommand.NEXT or data.command == PlayerCommand.PREVIOUS or data.command == PlayerCommand.REWIND or data.command == PlayerCommand.FASTFORWARD:
            value = data.command

        rospy.loginfo(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')
        log.info(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')

        self.oh.send_command(item, value)

    def RollershutterCallback(self, data):
        item = data.item

        if data.iscommand == True:
            if data.command == RollershutterCommand.UP or data.command == RollershutterCommand.DOWN or data.command == RollershutterCommand.STOP or data.command == RollershutterCommand.MOVE:
                value = data.command
        elif data.ispercentage == True:
            if 0 <= data.percentage <= 100:
                value = data.percentage

        rospy.loginfo(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')
        log.info(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')

        self.oh.send_command(item, value)

    def StringCallback(self, data):
        item = data.item

        if isinstance(data.command, str):
            value = data.command

        rospy.loginfo(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')
        log.info(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')

        self.oh.send_command(item, value)

    def SwitchCallback(self, data):
        item = data.item

        if data.command == SwitchCommand.ON or data.command == SwitchCommand.OFF:
            value = data.command

        rospy.loginfo(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')
        log.info(
            f'{rospy.get_caller_id()} Subscribed ROS topic /openhab/items/{item}/command with {value}')

        self.oh.send_command(item, value)


class LogItemStateRule(HABApp.Rule):
    """This rule logs the item state in the mqtt event bus log file"""

    def __init__(self):
        super().__init__()

        for item in self.get_items(type=OpenhabItem):
            item.listen_event(self.on_item_change, ValueChangeEvent)

    def on_item_change(self, event):
        assert isinstance(event, ValueChangeEvent)
        log.info(f'{event.name} changed from {event.old_value} to {event.value}')


OpenHABBridge()

# Create logger rule only if configured
if log_state:
    LogItemStateRule()
