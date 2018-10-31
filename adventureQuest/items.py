import random
import player

class Item:
  def __init__(self, name, description, value):
    self.name = name
    self.description = description
    self.value = value

  def __str__(self):
    return "{}\n======\n{}\nValue: {}".format(self.name, self.description, self.value)

##########################################################################################################

class Weapon(Item):
  def __init__(self, name, description, value, max_damage, max_quality, weapon_penalty):
    self.damage = max_damage
    self.max_damage = max_damage
    self.quality = max_quality
    self.max_quality = max_quality
    self.weapon_penalty = weapon_penalty
    super().__init__(name, description, value)

  def __str__(self):
    return super().__str__() + "\nDamage: {}\nQuality: {}".format(self.damage, self.quality)

  def repair(self, player):
    new_quality = random.randint(0, self.max_quality) + player.repair_skill
    confirm = input("Your repair skill is {}.\nAre you sure you want to attempt to repair it?\nYou may risk damaging it if you don't know what you are doing. [y/n]".format(player.repair_skill))
    if confirm.lower() == "y":
      start_quality = self.quality
      self.quality = new_quality
      if new_quality <= 0:
        print("Something went horribly wrong!")
      elif new_quality < start_quality:
        print("You apparently do not have much experience with {}s, as you have made it worse than it was before!".format(self.name))
      elif new_quality >= self.max_quality:
        player.repair_skill += 2
        player.xp_gain(5)
        print("You are a master of ingenuity!  You have repaired your {} to a level greater than any have ever thought possible!".format(self.name))
      elif new_quality > start_quality:
        player.repair_skill += 1
        player.xp_gain(2)
        print("You managed to improve the quality of your {} by some degree.  At least it is better than it was.".format(self.name))
      else:
        print("After inspecting further, you felt it wasn't the right time to try messing with your {}.  Maybe another day.".format(self.name))
      self.qualityCheck(player)

  def weardown(self, player):
    self.quality -= 1
    self.qualityCheck(player)

  def qualityCheck(self,player):
    if self.quality <= 0:
      self.shatter(player)
    elif self.quality <= 1:
      self.damage = self.max_damage - 3
      print("Your {} is about to break!  Repair it or use a different weapon!".format(self.name))
    elif self.quality <= 3:
      self.damage = self.max_damage - 1
      print("Your {} is showing some wear.  Consider repairing it.".format(self.name))
    elif self.quality > self.max_quality:
      self.damage = self.max_damage + 1
      print("Your {} is a shining example of quality, dealing slightly more damage than any other of its kind!".format(self.name))
    else:
      print("You notice your {} is not as fine as it once was, but it is still good at damaging things so you're not worried.".format(self.name)) 

  def shatter(self, player):
    player.remove_loot(self)
    print("Your {} has shattered!  You can no longer use or repair it, as it is now a pile of debris on the ground!".format(self.name))

class Dagger(Weapon):
  def __init__(self):
    super().__init__("Dagger", "A small rusty dagger with a blunt edge.  Quick and easy to use though", 5, 5, 15, 0)

class Club(Weapon):
  def __init__(self):
    super().__init__("Club", "A wooden club, good for bludgeoning.", 7, 8, 10, 1)

class Sword(Weapon):
  def __init__(self):
    super().__init__("Sword", "A sharp, well-balanced shortsword.  Keen and lethal.", 10, 10, 20, 2)
    

class BroadAxe(Weapon):
  def __init__(self):
    super().__init__("BroadAxe", "A massive axe!  Slow to swing but will cleave through anything it hits.", 15, 20, 20, 5)

##########################################################################################################

class Armour(Item):
  def __init__(self, name, description, value, max_protection, max_quality, armour_penalty):
    self.protection = max_protection
    self.max_protection = max_protection
    self.quality = max_quality
    self.max_quality = max_quality
    self.armour_penalty = armour_penalty
    super().__init__(name, description, value)

  def __str__(self):
    return super().__str__() + "\nProtection: {}\nQuality: {}".format(self.protection, self.quality)

  def repair(self, player):
    new_quality = random.randint(0, self.max_quality) + player.repair_skill
    confirm = input("Your repair skill is {}.\nAre you sure you want to attempt to repair it?\nYou may risk damaging it if you don't know what you are doing. [y/n]".format(player.repair_skill))
    if confirm.lower() == "y":
      start_quality = self.quality
      self.quality = new_quality
      if new_quality <= 0:
        print("Something went horribly wrong!")
      elif new_quality < start_quality:
        print("You apparently do not have much experience with {}s, as you have made it worse than it was before!".format(self.name))
      elif new_quality >= self.max_quality:
        player.repair_skill += 2
        player.xp_gain(5)
        print("You are a master of ingenuity!  You have repaired your {} to a level greater than any have ever thought possible!".format(self.name))
      elif new_quality > start_quality:
        player.repair_skill += 1
        player.xp_gain(2)
        print("You managed to improve the quality of your {} by some degree.  At least it is better than it was.".format(self.name))
      else:
        print("After inspecting further, you felt it wasn't the right time to try messing with your {}.  Maybe another day.".format(self.name))
      self.qualityCheck(player)

  def weardown(self, player):
    self.quality -= 1
    self.qualityCheck(player)

  def qualityCheck(self, player):
    if self.quality <= 0:
      self.shatter(player)
    elif self.quality <= 1:
      self.protection = self.max_protection - 3
      print("Your {} is about to break!  Repair it or use different armour!".format(self.name))
    elif self.quality <= 3:
      self.protection = self.max_protection - 1
      print("Your {} is showing some wear.  Consider repairing it.".format(self.name))
    elif self.quality > self.max_quality:
      self.protection = self.max_protection + 1
      print("Your {} is a shining example of quality, protecting you from slightly more damage than any other of its kind!".format(self.name))
    else:
      print("You notice your {} is not as fine as it once was, but it is still good at damaging things so you're not worried.".format(self.name)) 

  def shatter(self, player):
    player.remove_loot(self)
    print("Your {} has shattered!  You can no longer use or repair it, as it is now a pile of debris on the ground!".format(self.name))

class Cloth(Armour):
  def __init__(self):
    super().__init__("Cloth", "A tattered piece of cloth, barely able to cover you", 0, 0, 1, 0)

class LightArmour(Armour):
  def __init__(self):
    super().__init__("Light Armour", "A piece of studded cloth, providing some moderate protection without much impact to manuverability", 5, 3, 10, 0)

class HeavyArmour(Armour):
  def __init__(self):
    super().__init__("Heavy Armour", "A set of full plate armour, providing excellent protection but at the cost of speed", 20, 15, 20, 5)

class ChainMail(Armour):
  def __init__(self):
    super().__init__("Chain Mail", "A shirt of chain mail, providing decent protection but is a bit noisy", 10, 7, 10, 2)

##########################################################################################################

class StatIncrease(Item):
  def __init__(self, name, description, value, attr_affected, attr_increase):
    self.attr_affected = attr_affected
    self.attr_increase = attr_increase
    super().__init__(name, description, value)

  def __str__(self):
    return super().__str__() + "\nUse:  Adds {} to {}\n".format(self.attr_increase, self.attr_affected)

  def use(self, player):
    attr_val = getattr(player, self.attr_affected)
    setattr(player, self.attr_affected, attr_val + self.attr_increase)
    print("Your {} has increased by {} and is now {}".format(self.attr_affected, self.attr_increase, getattr(player,self.attr_affected)))
    
class SearchSkillBook(StatIncrease):
  def __init__(self):
    super().__init__("Search Skill Book","A book titled 'Finding Secret Rooms for Dummies'", 0, 'search_skill', 1)

##########################################################################################################

class Healing(Item):
  def __init__(self, name, description, value, hp_gain):
    self.hp_gain = hp_gain
    super().__init__(name, description, value)

  def use(self,player):
    if player.hp >= player.max_hp:
      print("You cannot use this as you are at max HP")
    elif player.hp > player.max_hp - self.hp_gain:
      player.hp = player.max_hp
    else:
      player.hp += self.hp_gain
    print("Your HP has increased by {} and is now {}".format(self.hp_gain, player.hp))
    
class SpiderMeat(Healing):
  def __init__(self):
    super().__init__("Spider Meat", "A chunk of tender meat from a Giant Spider.  Hope it's not poisonous", 1, 2)
    
class MinorHealthPotion(Healing):
  def __init__(self):
    super().__init__("Minor Health Potion", "A small vial of healing elixar.", 2, 5)

class HealthPotion(Healing):
  def __init__(self):
    super().__init__("Health Potion", "A strange brew.  Holding it feels invigorating", 5, 10)
##########################################################################################################

class DungeonKey(Item):
  def __init__(self):
    self.name = 'Dungeon Key'
    self.description = "A key with the word 'EXIT' printed on it.  I wonder what it will be used for ?"
    self.value = 0
