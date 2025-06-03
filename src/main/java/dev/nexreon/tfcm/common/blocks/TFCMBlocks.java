package dev.nexreon.tfcm.common.blocks;

import java.util.Map;
import java.util.function.Function;
import java.util.function.Supplier;

import javax.annotation.Nullable;

import dev.nexreon.tfcm.TFCMineralogy;
import dev.nexreon.tfcm.common.blocks.rock.TFCMOre;
import dev.nexreon.tfcm.common.fluids.TFCMSimpleFluid;
import dev.nexreon.tfcm.common.fluids.TFCMFluids;
import dev.nexreon.tfcm.common.items.TFCMItems;
import dev.nexreon.tfcm.util.TFCMMetal;

import net.dries007.tfc.common.blocks.ExtendedProperties;
import net.dries007.tfc.common.blocks.FluidCauldronBlock;
import net.dries007.tfc.common.blocks.rock.Rock;
import net.dries007.tfc.common.blocks.rotation.FluidPipeBlock;
import net.dries007.tfc.common.fluids.FluidId;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.registry.RegistrationHelpers;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LiquidBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour.Properties;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

public class TFCMBlocks {
    // Registering Ore Blocks :
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(Registries.BLOCK, TFCMineralogy.MODID);
    public static final Map<Rock, Map<TFCMOre, RegistryObject<Block>>> ORES = Helpers.mapOfKeys(Rock.class, rock ->
        Helpers.mapOfKeys(TFCMOre.class, ore -> !ore.isGraded(), ore ->
            register(("ore/" + ore.name() + "/" + rock.name()), () -> ore.create(rock))
        )
    );
    public static final Map<Rock, Map<TFCMOre, Map<TFCMOre.Grade, RegistryObject<Block>>>> GRADED_ORES = Helpers.mapOfKeys(Rock.class, rock ->
        Helpers.mapOfKeys(TFCMOre.class, TFCMOre::isGraded, ore ->
            Helpers.mapOfKeys(TFCMOre.Grade.class, grade ->
                register(("ore/" + grade.name() + "_" + ore.name() + "/" + rock.name()), () -> ore.create(rock))
            )
        )
    );
    // Registering Metals :
    public static final Map<TFCMMetal.Default, Map<TFCMMetal.BlockType, RegistryObject<Block>>> METALS = Helpers.mapOfKeys(TFCMMetal.Default.class, metal ->
        Helpers.mapOfKeys(TFCMMetal.BlockType.class, type -> type.has(metal), type ->
            register(type.createName(metal), type.create(metal), type.createBlockItem(new Item.Properties()))
        )
    );

    public static final Map<FluidId, RegistryObject<FluidCauldronBlock>> CAULDRONS = FluidId.mapOf(fluid ->
        registerNoItem("cauldron/" + fluid.name(), () -> new FluidCauldronBlock(Properties.copy(Blocks.CAULDRON)))
    );
    // Register Lead Pipe :
    public static final RegistryObject<Block> LEAD_PIPE = register("lead_pipe", () -> new FluidPipeBlock(ExtendedProperties.of().strength(5f).sound(SoundType.METAL)));
    
    // Register Molten Metals + TFCM Fluids:
    public static final Map<TFCMMetal.Default, RegistryObject<LiquidBlock>> METAL_FLUIDS = Helpers.mapOfKeys(TFCMMetal.Default.class, metal ->
        registerNoItem("fluid/metal/" + metal.name(), () -> new LiquidBlock(TFCMFluids.METALS.get(metal).source(), Properties.copy(Blocks.LAVA).noLootTable()))
    ); 
    public static final Map<TFCMSimpleFluid, RegistryObject<LiquidBlock>> SIMPLE_FLUIDS = Helpers.mapOfKeys(TFCMSimpleFluid.class, fluid ->
        registerNoItem("fluid/" + fluid.getId(), () -> new LiquidBlock(TFCMFluids.SIMPLE_FLUIDS.get(fluid).source(), Properties.copy(Blocks.WATER).noLootTable()))
    );
    // Private Methods for registration:
    private static <T extends Block> RegistryObject<T> registerNoItem(String name, Supplier<T> blockSupplier)
    {
        return register(name, blockSupplier, (Function<T, ? extends BlockItem>) null);
    }
    private static <T extends Block> RegistryObject<T> register(String name, Supplier<T> blockSupplier)
    {
        return register(name, blockSupplier, block -> new BlockItem(block, new Item.Properties()));
    }

    private static <T extends Block> RegistryObject<T> register(String name, Supplier<T> blockSupplier, @Nullable Function<T, ? extends BlockItem> blockItemFactory)
    {
        return RegistrationHelpers.registerBlock(TFCMBlocks.BLOCKS, TFCMItems.ITEMS, name, blockSupplier, blockItemFactory);
    }
}
