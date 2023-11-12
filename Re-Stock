# define drag_time
drag_time = 1000

# define reg ItemID
black_pearl = 0x0F7A
nightshade = 0x0F88
sulfurous_ash = 0x0F8C
ginseng = 0x0F85
blood_moss = 0x0F7B
mandrake_root = 0x0F86
garlic = 0x0F84
spider_silk = 0x0F8D
bandages = 0x0E21
daemons = 0x1F69

#define potion ItemID
greater_heal = 0x0F0C
greater_cure = 0x0F07
greater_strength = 0x0F09
greater_refresh = 0x0F0B
greater_explosion = 0x0F0D
empty_bottle = 0x0F0E

# define restock container serial
resupply_container = 0x42536F43

# define player backpack serial
player_backpack = 0x4047F03F

# set target values
target_black_pearl = 100
target_nightshade = 100
target_sulfurous_ash = 30 
target_ginseng = 30
target_blood_moss = 100
target_mandrake_root = 100
target_garlic = 30
target_spider_silk = 50
target_daemons = 8
target_bandages = 0
target_heal = 5
target_cure = 5
target_strength = 5
target_refresh = 5
target_explosion = 0
target_empty_bottle = 0

# get player values
player_black_pearl = Items.BackpackCount(black_pearl,-1)
player_nightshade = Items.BackpackCount(nightshade,-1)
player_sulfurous_ash = Items.BackpackCount(sulfurous_ash,-1)
player_ginseng = Items.BackpackCount(ginseng,-1)
player_blood_moss = Items.BackpackCount(blood_moss,-1)
player_mandrake_root = Items.BackpackCount(mandrake_root,-1)
player_garlic = Items.BackpackCount(garlic,-1)
player_spider_silk = Items.BackpackCount(spider_silk,-1)
player_daemons = Items.BackpackCount(daemons,-1)
player_bandages = Items.BackpackCount(bandages,-1)
player_heal = Items.BackpackCount(greater_heal,-1)
player_cure = Items.BackpackCount(greater_cure,-1)
player_strength = Items.BackpackCount(greater_strength,-1)
player_refresh = Items.BackpackCount(greater_refresh,-1)
player_explosion = Items.BackpackCount(greater_explosion,-1)
player_empty_bottle = Items.BackpackCount(empty_bottle,-1)

# get restock container values
restock_black_pearl = Items.ContainerCount(resupply_container,black_pearl,-1,False)
restock_nightshade = Items.ContainerCount(resupply_container,nightshade,-1,False)
restock_sulfurous_ash = Items.ContainerCount(resupply_container,sulfurous_ash,-1,False)
restock_ginseng = Items.ContainerCount(resupply_container,ginseng,-1,False)
restock_blood_moss = Items.ContainerCount(resupply_container,blood_moss,-1,False)
restock_mandrake_root = Items.ContainerCount(resupply_container,mandrake_root,-1,False)
restock_garlic = Items.ContainerCount(resupply_container,garlic,-1,False)
restock_spider_silk = Items.ContainerCount(resupply_container,spider_silk,-1,False)
restock_daemons = Items.ContainerCount(resupply_container,daemons,-1,False)
restock_bandages = Items.ContainerCount(player_backpack,bandages,-1,False)
restock_heal = Items.ContainerCount(player_backpack,greater_heal,-1,False)
restock_cure = Items.ContainerCount(player_backpack,greater_cure,-1,False)
restock_strength = Items.ContainerCount(player_backpack,greater_strength,-1,False)
restock_refresh = Items.ContainerCount(player_backpack,greater_refresh,-1,False)
restock_explosion = Items.ContainerCount(player_backpack,greater_explosion,-1,False)
restock_empty_bottle = Items.ContainerCount(player_backpack,empty_bottle,-1,False)

# open all pouches for accurate counts
for i in Player.Backpack.Contains:
    if i.ItemID == 0x0E76:
        Items.UseItem(i)
        Misc.Pause(1000)
        
Misc.Pause(1000)

# offload weapons & armor
Restock.RunOnce("unload_wepsarmor",player_backpack,0x42536E9C,800)

Restock.RunOnce("unload_treasure",player_backpack,0x42536CB8,800)

def restockRegs(reg_id, player_reg_count, target_reg_count, reg_name):
    if player_reg_count < target_reg_count:
        reg_to_move = target_reg_count - player_reg_count
        reg_found = Items.FindByID(reg_id,-1,resupply_container,False,True)
        if reg_found:
            Items.Move(reg_found,player_backpack,reg_to_move)
            Misc.Pause(drag_time)
        else:
            Player.HeadMessage(75, "Resupply Container Out of " + reg_name)
    elif player_reg_count > target_reg_count:
        reg_to_move = player_reg_count - target_reg_count
        reg_found = Items.FindByID(reg_id,-1,player_backpack,True,True)
        if reg_found:
            Items.Move(reg_found,resupply_container,reg_to_move)
            Misc.Pause(drag_time)
        else:
            Player.HeadMessage(75, "Backpack Out of " + reg_name)       
            
Items.UseItem(resupply_container)
Misc.Pause(1000)
restockRegs(black_pearl, player_black_pearl, target_black_pearl, "Black Pearl")
restockRegs(nightshade, player_nightshade, target_nightshade, "Nightshade")
restockRegs(sulfurous_ash, player_sulfurous_ash, target_sulfurous_ash, "Sulfurous Ash")
restockRegs(ginseng, player_ginseng, target_ginseng, "Ginseng")
restockRegs(blood_moss, player_blood_moss, target_blood_moss, "Blood Moss")
restockRegs(mandrake_root, player_mandrake_root, target_mandrake_root, "Mandrake Root")
restockRegs(garlic, player_garlic, target_garlic, "Garlic")
restockRegs(spider_silk, player_spider_silk, target_spider_silk, "Spider Silk")
restockRegs(daemons, player_daemons, target_daemons, "Daemon Scrolls")
restockRegs(bandages, player_bandages, target_bandages, "Bandages")
restockRegs(greater_heal, player_heal, target_heal, "Greater Heal")
restockRegs(greater_cure, player_cure, target_cure, "Greater Cure")
restockRegs(greater_strength, player_strength, target_strength, "Greater Strength")
restockRegs(greater_refresh, player_refresh, target_refresh, "Greater Refresh")
restockRegs(greater_explosion, player_explosion, target_explosion, "Greater Explosion")
restockRegs(empty_bottle, player_empty_bottle, target_empty_bottle, "Empty Bottle")
Items.Close(resupply_container)
Misc.Pause(2000)
Player.ChatSay(75,"[organizeme")
Player.HeadMessage(75,"Restock complete.")
