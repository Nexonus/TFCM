package dev.nexreon.tfcmineralogy.init;

import java.rmi.registry.Registry;
import dev.nexreon.tfcmineralogy.TFCMineralogy;
import net.minecraftforge.common.Tags.Items;
import net.minecraftforge.fml.common.Mod;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.level.block.Block;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import static dev.nexreon.tfcmineralogy.init.CreativeTabInit.addToTab;

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
        for (StoneType stone : StoneType.values()){
            for (MineralType mineral : MineralType.values()){
                String blockName = stone.getSerializedName() + "_" + mineral.getSerializedName();
                RegistryObject<Block> correspondingBlock = BlockInit.MINERAL_ORES.get(blockName);

                RegistryObject<BlockItem> ORE_BLOCK_ITEM = addToTab(ITEMS.register(blockName,
                () -> new BlockItem(correspondingBlock.get(), new Item.Properties()
                .rarity(Rarity.COMMON))));
            }
        }
    }
}
