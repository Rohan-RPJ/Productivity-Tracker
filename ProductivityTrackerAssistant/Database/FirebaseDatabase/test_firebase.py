from . import db


all_ids = db.child("wd").shallow().get()
print(all_ids.val())