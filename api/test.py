from lib.profile_generator import StatusTile

test = StatusTile(icon_path="../image/icon/camera.png", title="スクショ撮影")

test.get_status_tile("許可").show()
