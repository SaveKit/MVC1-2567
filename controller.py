class CowController:
    def __init__(self, model):
        self.model = model

    def find_cow(self, cow_id):
        return self.model.get_cow(cow_id)

    def milk_cow(self, cow_id):
        cow = self.model.produce_milk(cow_id)
        self.model.save_cows()
        return cow

    def milk_cow_with_lemon(self, cow_id):
        cow = self.model.produce_milk(cow_id, lemon=True)
        self.model.save_cows()
        return cow

    def reset_cow(self, cow_id):
        cow = self.model.reset_bsod(cow_id)
        self.model.save_cows()
        return cow
