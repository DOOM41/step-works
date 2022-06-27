from field import Field
import tools

player_1 = Field()
enemy = Field()
player_1.manual_placement()
enemy.random_placement()
print(enemy)
print(player_1)

