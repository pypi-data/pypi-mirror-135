def deserialize_avro(msg, schema):
    import io
    import fastavro

    bytes_io = io.BytesIO(msg)
    bytes_io.seek(0)

    deserialized_msg = fastavro.schemaless_reader(bytes_io, schema)
    return deserialized_msg
