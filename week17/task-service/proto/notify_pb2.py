from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0cnotify.proto\x12\x06notify"\xa7\x01\n\nTaskUpdate\x12\x0f\n\x07task_id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x12\n\nold_status\x18\x03 \x01(\t\x12\x12\n\nnew_status\x18\x04 \x01(\t\x12\x12\n\nuser_email\x18\x05 \x01(\t\x12\x11\n\ttimestamp\x18\x06 \x01(\x03\x12\x30\n\x08metadata\x18\x07 \x03(\x0b\x32\x1e.notify.TaskUpdate.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"`\n\x14NotificationResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x17\n\x0fnotification_id\x18\x03 \x01(\t\x12\x0f\n\x07sent_at\x18\x04 \x01(\x03\x32\xaa\x01\n\x0eNotifyService\x12\x46\n\x11SendNotification\x12\x12.notify.TaskUpdate\x1a\x1c.notify.NotificationResponse"\x00\x12P\n\x14StreamNotifications\x12\x12.notify.TaskUpdate\x1a\x1c.notify.NotificationResponse"\x00(\x01\x30\x01\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'notify_pb2', _globals)

if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_TASKUPDATE_METADATAENTRY']._options = None
    _globals['_TASKUPDATE_METADATAENTRY']._serialized_options = b'8\x01'
    _globals['_TASKUPDATE']._serialized_start = 25
    _globals['_TASKUPDATE']._serialized_end = 192
    _globals['_TASKUPDATE_METADATAENTRY']._serialized_start = 145
    _globals['_TASKUPDATE_METADATAENTRY']._serialized_end = 192
    _globals['_NOTIFICATIONRESPONSE']._serialized_start = 194
    _globals['_NOTIFICATIONRESPONSE']._serialized_end = 290
    _globals['_NOTIFYSERVICE']._serialized_start = 293
    _globals['_NOTIFYSERVICE']._serialized_end = 463