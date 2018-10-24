import items
import world


class NonPlayableCharacter():
    def __init__(self):
        raise NotImplementedError("Do not create raw NPC objects.")

    def __str__(self):
        return self.name


class Trader(NonPlayableCharacter):
    def __init__(self):
        self.name = "Trader"
		
	def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell, or (Q)uit?")
            user_input = input()
            if user_input.upper() == "Q":
                return
            elif user_input.upper() == "B":
                print("Here's whats available to buy: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input.upper() == "S":
                print("Here's whats available to sell: ")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid choice!")

    def buy(self, buyer):
        for i, item in enumerate(world.trade_inventory, 1):
            if item.name <> "Gold":
				print("{}. {} - {} Gold".format(i, item.name, item.value))
        while True:
            user_input = input("Choose an item or press Q to exit: ")
            if user_input.upper() == "Q":
                return
            else:
                try:
                    choice = int(user_input)
                    to_buy = world.trade_inventory[choice - 1]
                    if to_buy.value > buyer.gold:
						print("You don't have enough gold for that")
						return
					else:
						buyer.gold -= to_buy.value
						world.trade_inventory["Gold"] += to_buy.value
						world.trade_inventory.remove(to_buy)
						buyer.inventory.append(to_buy)
						print("You bought a new {}!  You now have {} gold remaining.".format(to_buy.name,buyer.gold.value))
                except ValueError:
                    print("Invalid choice!")

    def sell(self, seller):
        for i, item in enumerate(seller.inventory, 1):
            if item.name <> "Gold":
				print("{}. {} - {} Gold".format(i, item.name, round(item.value*.6,0)))
        while True:
            user_input = input("Choose an item or press Q to exit: ")
            if user_input.upper() == "Q":
                return
            else:
                try:
                    choice = int(user_input)
                    to_buy = seller.inventory[choice - 1]
					price = round(to_buy.value*0.6,0)
                    if price > world.trade_inventory["Gold"]:
						print("I don't have enough gold for that")
						return
					else:
						seller.gold += price
						world.trade_inventory["Gold"] -= price
						seller.inventory.remove(to_buy)
						world.trade_inventory.append(to_buy)
						print("You sold your {}!  You now have {} gold remaining.".format(to_buy.name,seller.gold.value))
                except ValueError:
                    print("Invalid choice!")