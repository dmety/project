from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.config import settings


def init_milvus():
    try:
        connections.connect(
            host=settings.MILVUS_HOST,
            port=settings.MILVUS_PORT
        )
        print("成功连接到Milvus")

        knowledge_embedding_fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="knowledge_id", dtype=DataType.INT64),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
            FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=2048)
        ]

        knowledge_embedding_schema = CollectionSchema(
            fields=knowledge_embedding_fields,
            description="知识点向量存储"
        )

        if not utility.has_collection("knowledge_embedding"):
            knowledge_embedding_collection = Collection(
                name="knowledge_embedding",
                schema=knowledge_embedding_schema
            )
            print("创建知识点向量集合成功")

            index_params = {
                "index_type": "IVF_FLAT",
                "metric_type": "IP",
                "params": {"nlist": 1024}
            }
            knowledge_embedding_collection.create_index(
                field_name="embedding",
                index_params=index_params
            )
            print("创建知识点向量索引成功")
        else:
            print("知识点向量集合已存在")

        user_profile_embedding_fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="user_id", dtype=DataType.INT64),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
            FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=2048)
        ]

        user_profile_embedding_schema = CollectionSchema(
            fields=user_profile_embedding_fields,
            description="用户画像向量存储"
        )

        if not utility.has_collection("user_profile_embedding"):
            user_profile_embedding_collection = Collection(
                name="user_profile_embedding",
                schema=user_profile_embedding_schema
            )
            print("创建用户画像向量集合成功")

            index_params = {
                "index_type": "IVF_FLAT",
                "metric_type": "IP",
                "params": {"nlist": 1024}
            }
            user_profile_embedding_collection.create_index(
                field_name="embedding",
                index_params=index_params
            )
            print("创建用户画像向量索引成功")
        else:
            print("用户画像向量集合已存在")

        print("Milvus初始化完成")

    except Exception as e:
        print(f"Milvus初始化失败: {e}")
        sys.exit(1)
    finally:
        connections.disconnect("default")


if __name__ == "__main__":
    init_milvus()
