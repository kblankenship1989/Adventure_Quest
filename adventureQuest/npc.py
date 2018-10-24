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
                    if to_buy.value > buyer.check_gold():
						print("You don't have enough gold for that"
                except ValueError:
                    print("Invalid choice!")

    def sell(self, seller):
        if item.value > buyer.gold:
            print("That's too expensive")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold = seller.gold + item.value
        buyer.gold = buyer.gold - item.value
        print("Trade complete!")
