# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: audio.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='audio.proto',
  package='audioRPC',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0b\x61udio.proto\x12\x08\x61udioRPC\"\x1f\n\x06nombre\x12\x15\n\rnombreJugador\x18\x01 \x01(\t\"5\n\x05lista\x12\x15\n\rnombreJugador\x18\x01 \x01(\t\x12\x15\n\rnumeroJugador\x18\x02 \x01(\x05\"\x1c\n\x0btrozosAudio\x12\r\n\x05\x63hunk\x18\x01 \x01(\x0c\"q\n\x12respuestaPersonaje\x12\x0e\n\x06\x65stado\x18\x01 \x01(\x08\x12\x12\n\ntextoAudio\x18\x02 \x01(\t\x12\x11\n\trespuesta\x18\x03 \x01(\x08\x12\x0e\n\x06nombre\x18\x04 \x01(\t\x12\x14\n\x0ctextoPartida\x18\x05 \x01(\t2\x80\x02\n\x05\x41udio\x12\x33\n\x0ciniciarJuego\x12\x10.audioRPC.nombre\x1a\x0f.audioRPC.lista\"\x00\x12\x35\n\rterminarJuego\x12\x10.audioRPC.nombre\x1a\x10.audioRPC.nombre\"\x00\x12\x42\n\x0f\x61\x63tualizarJuego\x12\x0f.audioRPC.lista\x1a\x1c.audioRPC.respuestaPersonaje\"\x00\x12G\n\x0crecibirAudio\x12\x15.audioRPC.trozosAudio\x1a\x1c.audioRPC.respuestaPersonaje\"\x00(\x01\x62\x06proto3'
)




_NOMBRE = _descriptor.Descriptor(
  name='nombre',
  full_name='audioRPC.nombre',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='nombreJugador', full_name='audioRPC.nombre.nombreJugador', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=56,
)


_LISTA = _descriptor.Descriptor(
  name='lista',
  full_name='audioRPC.lista',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='nombreJugador', full_name='audioRPC.lista.nombreJugador', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='numeroJugador', full_name='audioRPC.lista.numeroJugador', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=58,
  serialized_end=111,
)


_TROZOSAUDIO = _descriptor.Descriptor(
  name='trozosAudio',
  full_name='audioRPC.trozosAudio',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='chunk', full_name='audioRPC.trozosAudio.chunk', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=113,
  serialized_end=141,
)


_RESPUESTAPERSONAJE = _descriptor.Descriptor(
  name='respuestaPersonaje',
  full_name='audioRPC.respuestaPersonaje',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='estado', full_name='audioRPC.respuestaPersonaje.estado', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='textoAudio', full_name='audioRPC.respuestaPersonaje.textoAudio', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='respuesta', full_name='audioRPC.respuestaPersonaje.respuesta', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nombre', full_name='audioRPC.respuestaPersonaje.nombre', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='textoPartida', full_name='audioRPC.respuestaPersonaje.textoPartida', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=143,
  serialized_end=256,
)

DESCRIPTOR.message_types_by_name['nombre'] = _NOMBRE
DESCRIPTOR.message_types_by_name['lista'] = _LISTA
DESCRIPTOR.message_types_by_name['trozosAudio'] = _TROZOSAUDIO
DESCRIPTOR.message_types_by_name['respuestaPersonaje'] = _RESPUESTAPERSONAJE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

nombre = _reflection.GeneratedProtocolMessageType('nombre', (_message.Message,), {
  'DESCRIPTOR' : _NOMBRE,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audioRPC.nombre)
  })
_sym_db.RegisterMessage(nombre)

lista = _reflection.GeneratedProtocolMessageType('lista', (_message.Message,), {
  'DESCRIPTOR' : _LISTA,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audioRPC.lista)
  })
_sym_db.RegisterMessage(lista)

trozosAudio = _reflection.GeneratedProtocolMessageType('trozosAudio', (_message.Message,), {
  'DESCRIPTOR' : _TROZOSAUDIO,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audioRPC.trozosAudio)
  })
_sym_db.RegisterMessage(trozosAudio)

respuestaPersonaje = _reflection.GeneratedProtocolMessageType('respuestaPersonaje', (_message.Message,), {
  'DESCRIPTOR' : _RESPUESTAPERSONAJE,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audioRPC.respuestaPersonaje)
  })
_sym_db.RegisterMessage(respuestaPersonaje)



_AUDIO = _descriptor.ServiceDescriptor(
  name='Audio',
  full_name='audioRPC.Audio',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=259,
  serialized_end=515,
  methods=[
  _descriptor.MethodDescriptor(
    name='iniciarJuego',
    full_name='audioRPC.Audio.iniciarJuego',
    index=0,
    containing_service=None,
    input_type=_NOMBRE,
    output_type=_LISTA,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='terminarJuego',
    full_name='audioRPC.Audio.terminarJuego',
    index=1,
    containing_service=None,
    input_type=_NOMBRE,
    output_type=_NOMBRE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='actualizarJuego',
    full_name='audioRPC.Audio.actualizarJuego',
    index=2,
    containing_service=None,
    input_type=_LISTA,
    output_type=_RESPUESTAPERSONAJE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='recibirAudio',
    full_name='audioRPC.Audio.recibirAudio',
    index=3,
    containing_service=None,
    input_type=_TROZOSAUDIO,
    output_type=_RESPUESTAPERSONAJE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_AUDIO)

DESCRIPTOR.services_by_name['Audio'] = _AUDIO

# @@protoc_insertion_point(module_scope)
