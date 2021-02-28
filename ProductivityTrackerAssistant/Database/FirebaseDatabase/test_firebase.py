from . import db


all_ids = db.child("istt").child(123).get().val()
print(list(all_ids.values()))