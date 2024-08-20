import object_classes as obj


# Functions
# Def create level
def decipher(level_list, level_group):
    for a in level_list:
        if a[0] == 'BB':
            level_group.add(obj.BlueBlock(a[1], a[2]))
        elif a[0] == 'YB':
            level_group.add(obj.YellowBlock(a[1], a[2]))
        elif a[0] == 'GB':
            level_group.add(obj.GreenBlock(a[1], a[2]))
        elif a[0] == 'RB':
            level_group.add(obj.RedBlock(a[1], a[2]))
        elif a[0] == 'IM':
            level_group.add(obj.Immovable(a[1], a[2]))
        elif a[0] == 'MB':
            level_group.add(obj.Moving(a[1], a[2]))


# Creating except_ball_group
def create_except_ball(ball, lv_group, except_ball):
    for sp in lv_group:
        if sp != ball:
            except_ball.add(sp)