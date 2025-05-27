package dev.nexreon.tfcmineralogy.init;

import java.rmi.registry.Registry;
import java.util.HashMap;
import java.util.Map;

import dev.nexreon.tfcmineralogy.TFCMineralogy;
import net.minecraftforge.common.Tags.Blocks;
import net.minecraftforge.fml.common.Mod;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;
import net.minecraft.world.level.block.SoundType;


public class BlockInit {
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(ForgeRegistries.BLOCKS, TFCMineralogy.MODID);
    public static final RegistryObject<Block> EXAMPLE_BLOCK = BLOCKS.register("example_block", 
    () -> new Block(BlockBehaviour.Properties.of()
    .mapColor(MapColor.COLOR_GRAY)
    .strength(6.0F)
    .sound(SoundType.STONE)
    .requiresCorrectToolForDrops()));

    public static final Map<String, RegistryObject<Block>> MINERAL_ORES = new HashMap<>();

    static{
        for (StoneType stone : StoneType.values()){
            for (MineralType mineral : MineralType.values()){
                String blockName = stone.getSerializedName() + "_" + mineral.getSerializedName();
                RegistryObject<Block> ORE_BLOCK = BLOCKS.register(blockName, 
                () -> new Block(BlockBehaviour.Properties.of()
                .mapColor(mineral.getBaseMapColor())
                .strength(mineral.getBlockStrength())
                .sound(SoundType.STONE)
                .requiresCorrectToolForDrops()));

                MINERAL_ORES.put(blockName, ORE_BLOCK);
            }
        }
    }
}
