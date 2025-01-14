import pygame
from unit import Unit
#from copy import deepcopy
from player import Player
from text import Text
class Village(Unit,pygame.sprite.Sprite):
    def __init__(self,owner1,vill_type,starting_rect) -> None:   #if type is 60 village is a city, owner 0 is no one's villge
        super(Village,self).__init__()
        self.owner = owner1
        self.vill_type = vill_type
        self.selected = False
        self.can_conscript_turns = 4
        #self.rect = starting_rect.copy()
        if vill_type == 60:
            self.base_health = 225
            self.base_defence = 30
            self.p_gold = 5
            self.p_spear = 2
            self.p_food = -3
            self.p_bow = 0
            self.p_lumber = -2
            self.banner = pygame.image.load("images/city.png")
        else:
            self.base_health = 33
            self.base_defence = 6
        if vill_type == 1:
            self.p_lumber = 5
            self.p_food = -1
            self.p_bow = 0
            self.p_gold = 0.1
            self.p_spear = 0
            self.banner = pygame.image.load("images/village_lumber.png")
        if vill_type == 2:
            self.p_lumber = 0
            self.p_food = 5
            self.p_bow = 0
            self.p_gold = 0.1
            self.p_spear = 0
            self.banner = pygame.image.load("images/village_food.png")
        if vill_type == 3:
            self.p_lumber = -1
            self.p_food = -1
            self.p_bow = 0
            self.p_gold = 0.15
            self.p_spear = 1
            self.banner = pygame.image.load("images/village_spear.png")
        if vill_type == 4:
            self.p_lumber = -1.05
            self.p_food = -1
            self.p_bow = 1
            self.p_gold = 0.15
            self.p_spear = 0
            self.banner = pygame.image.load("images/village_bow.png")
        if vill_type == 5:
            self.p_lumber = -1
            self.p_food = -2
            self.p_bow = 0
            self.p_gold = 10
            self.p_spear = 0
            self.banner = pygame.image.load("images/village_gold.png")
        self.health = self.base_health
        self.rect = self.banner.get_rect(bottomleft=starting_rect)
        self.x = starting_rect[0]
        self.y = starting_rect[1]
        self.new_banner = self.banner
        #TEMPORARY!
        self.anti_infantry_bonus = 0
        self.anti_cav_bonus = 0
    def select_village(self,villages,texts):
        for vil in villages:
            vil.selected = False
        if self.selected:
            self.selected = False
            Text.add_text(texts,"Village unselected!")
        else:
            self.selected = True
            Text.add_text(texts,"Village selected!")
    def unselect_villages(villages,texts):
        Text.add_text(texts,"All villages unselected!")
        for vil in villages:
            vil.selected = False
        
    def locate_village(type,owner,starting_rect,free_location=False,texts=None):
        player = owner
        location_possible = False
        new_village = None
        if free_location == False:
            if type != 5:
                if player.gold >= 2 and player.lumber >= 5:
                    location_possible = True
                    player.gold -= 2
                    player.lumber -= 5
                else:
                    if texts is not None:
                        Text.add_text(texts,"Our stocks are too low!")
            elif type == 5:
                if player.gold >= 10 and player.lumber >= 8 and player.food >= 1:
                    player.gold -= 10
                    player.lumber -= 8
                    player.food -= 1
                    location_possible = True
                else:
                    if texts is not None:
                        Text.add_text(texts,"Our stocks are too low!")
        else:
            location_possible = True
        if location_possible:
            if texts is not None:
                Text.add_text(texts,"Village_founded!")
            new_village = Village(owner,type,starting_rect)
            return new_village
                
    """
    def check_production_global(villages,players):
        for p in players:
            p.reset_production
        for vil in villages:
            vil.owner.p_gold += vil.p_gold
            vil.owner.p_lumber += vil.p_lumber
            vil.owner.p_food += vil.p_food
            vil.owner.p_spear += vil.p_spear
            vil.owner.p_bow += vil.p_bow"""
    def turns_left_change(villages):
        for vil in villages:
            if vil.can_conscript_turns > 0:
                vil.can_conscript_turns -= 1
    def change_owner(self,new_owner,texts):
        self.owner.villages.remove(self)
        self.owner = new_owner
        new_owner.get_villaged(self)
        Text.add_text(texts,f"Village conquered by {new_owner.name}!")