package dev.nexreon.tfcmineralogy.init;

import dev.nexreon.tfcmineralogy.TFCMineralogy;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.level.block.Block;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import static dev.nexreon.tfcmineralogy.init.CreativeTabInit.addToTab;

import org.jline.utils.Log;

public class ItemInit {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, TFCMineralogy.MODID);
    public static final RegistryObject<Item> EXAMPLE_ITEM = addToTab(ITEMS.register("example_item",
        () -> new Item(new Item.Properties()
        .stacksTo(64)
        .rarity(Rarity.COMMON))));
    
    public static final RegistryObject<BlockItem> EXAMPLE_BLOCK_ITEM = addToTab(ITEMS.register("example_block",
        () -> new BlockItem(BlockInit.EXAMPLE_BLOCK.get(), new Item.Properties()
        .rarity(Rarity.COMMON))));


    static{
        for (ResourceEnums stone : ResourceEnums.values()){
            for (MineralType mineral : MineralType.values()){
                String blockName = "ore/" + mineral.getSerializedName() + "/" + stone.getSerializedName();
                String itemName = "ore/" + mineral.getSerializedName();
                try{
                RegistryObject<Block> correspondingBlock = BlockInit.MINERAL_ORES.get(blockName);

                RegistryObject<BlockItem> ORE_BLOCK_ITEM = addToTab(ITEMS.register(blockName,
                () -> new BlockItem(correspondingBlock.get(), new Item.Properties()
                .rarity(Rarity.COMMON)))); // Register Block Item

                RegistryObject<Item> ORE_ITEM = addToTab(ITEMS.register(itemName,
                () -> new Item(new Item.Properties()
                .rarity(Rarity.COMMON))));
                }
                catch(Exception e){
                    Log.error("No Corresponding Block! @ITEMINIT");
                }
            }
        }
        for (PowderType powder : PowderType.values()){
            String powderName = powder.getSerializedName();
            RegistryObject<Item> ORE_POWDER = addToTab(ITEMS.register(powderName,
                () -> new Item(new Item.Properties()
                .rarity(Rarity.COMMON))));
        }
    }
}
