import items
import player as Player
import random

class Enemy:
  def __init__(self, name, base_max_hp, max_hp_per_lvl, base_damage, damage_per_lvl, base_protection, protection_per_level, base_initiative, initiative_per_lvl, base_xp, xp_per_lvl, level, has_special = False):
    self.name = name
    self.max_hp = base_max_hp + round(max_hp_per_lvl*level,0)
	self.hp = self.max_hp
    self.damage = base_damage + round(damage_per_lvl*level,0)
    self.protection = base_protection + round(protection_per_lvl*level,0)
    self.initiative = base_initiative + round(initiative_per_lvl*level,0)
	self.xp = base_xp + round(xpper_lvl*level,0)
	self.level = level
	#self.has_special = has_special
	self.loot = []

  def is_alive(self):
    return self.hp > 0
	
  def __str__(self):
    return "{} (lvl {})\nHP: {}/{}\n".format(self.name,self.level,self.hp,self.max_hp)
	
  #def special_attack(self, player, method):
    # if self.has_special:
      # use_special = random.randint(0, 9) >= 8
	  # if use_special:
        # __special_method = getattr(self, method.__name__)
    # if __special_method:
      # __special_method(player)
	  
  def examine_body(self, player):
    if not self.is_alive():
	  amt =  random.randint(0,50)
      if amt > 0:  self.loot.append(items.Gold(amt))
    
class GiantSpider(Enemy):
  def __init__(self, level):
    super().__init__(name = "Giant Spider"
	                 , base_max_hp = 10
					 , max_hp_per_lvl = 2
					 , base_damage = 5
					 , damage_per_lvl = 1
					 , base_protection = 5
					 , protection_per_level = 1
					 , base_initiative = 5
					 , base_xp = 3
					 , xp_per_lvl = 1
					 , initiative_per_lvl = 0.2
					 , level = level)

class Goblin(Enemy):
  def __init__(self, level):
    super().__init__(name = "Goblin"
	                 , base_max_hp = 5
					 , max_hp_per_lvl = 1
					 , base_damage = 3
					 , damage_per_lvl = 1
					 , base_protection = 1
					 , protection_per_level = 0.5
					 , base_initiative = 5
					 , base_xp = 1
					 , xp_per_lvl = .5
					 , initiative_per_lvl = 0.1
					 , level = level)
	
class RatSwarm(Enemy):
  def __init__(self):
    super().__init__('Rat', 2, 2, 0, 3)
	
  def __init__(self, level):
    super().__init__(name = "Giant Spider"
	                 , base_max_hp = 10
					 , max_hp_per_lvl = 2
					 , base_damage = 5
					 , damage_per_lvl = 1
					 , base_protection = 5
					 , protection_per_level = 1
					 , base_initiative = 5
					 , base_xp = 3
					 , xp_per_lvl = 1
					 , initiative_per_lvl = 0.2
					 , level = level)
					 
class Ogre(Enemy):
  def __init__(self, level):
    super().__init__(name = "Giant Spider"
	                 , base_max_hp = 10
					 , max_hp_per_lvl = 2
					 , base_damage = 5
					 , damage_per_lvl = 1
					 , base_protection = 5
					 , protection_per_level = 1
					 , base_initiative = 5
					 , base_xp = 3
					 , xp_per_lvl = 1
					 , initiative_per_lvl = 0.2
					 , level = level)