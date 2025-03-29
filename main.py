from pymongo import MongoClient
from bson.objectid import ObjectId

client: MongoClient = MongoClient(
    "mongodb+srv://filzenoviy:e3SJs6CErAZbRwMy@cluster0.hyrtfpe.mongodb.net/"
)

db = client["cats_db"]
cats_collection = db["cats"]


def add_cat(name: str, age: int, features: list):
    cat = {"name": name, "age": age, "features": features}
    cats_collection.insert_one(cat)
    print(f"Додано кота: {name}")


def get_all_cats():
    for cat in cats_collection.find():
        print(cat)


def get_cat_by_name(name: str):
    cat = cats_collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"Кіт з ім'ям {name} не знайдений")


def update_cat_age(name: str, new_age: int):
    result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.modified_count:
        print(f"Оновлено вік кота {name} до {new_age}")
    else:
        print(f"Кіт {name} не знайдений")


def add_feature_to_cat(name: str, feature: str):
    result = cats_collection.update_one(
        {"name": name}, {"$push": {"features": feature}}
    )
    if result.modified_count:
        print(f"Додано характеристику '{feature}' коту {name}")
    else:
        print(f"Кіт {name} не знайдений")


def delete_cat_by_name(name: str):
    result = cats_collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"Кіт {name} видалений")
    else:
        print(f"Кіт {name} не знайдений")


def delete_all_cats():
    cats_collection.delete_many({})
    print("Всі коти видалені")


if __name__ == "__main__":
    add_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    add_cat("black", 5, ["ходить в капці", "дає себе гладити", "рудий"])
    add_cat("white", 7, ["ходить в капці", "дає себе гладити", "рудий"])
    add_cat("green", 12, ["ходить в капці", "дає себе гладити", "рудий"])
    get_all_cats()
    get_cat_by_name("barsik")
    update_cat_age("barsik", 4)
    add_feature_to_cat("barsik", "любить гратися з м'ячиком")
    delete_cat_by_name("barsik")
    delete_all_cats()
