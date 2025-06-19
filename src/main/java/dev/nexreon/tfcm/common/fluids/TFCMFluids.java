package dev.nexreon.tfcm.common.fluids;

import java.util.Map;
import java.util.function.Consumer;
import java.util.function.Function;

import dev.nexreon.tfcm.TFCMineralogy;
import dev.nexreon.tfcm.common.blocks.TFCMBlocks;
import dev.nexreon.tfcm.common.items.TFCMItems;
import dev.nexreon.tfcm.util.TFCMMetal;
import net.dries007.tfc.common.fluids.ExtendedFluidType;
import net.dries007.tfc.common.fluids.FluidRegistryObject;
import net.dries007.tfc.common.fluids.FluidTypeClientProperties;
import net.dries007.tfc.common.fluids.MixingFluid;
import net.dries007.tfc.common.fluids.MoltenFluid;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.registry.RegistrationHelpers;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.level.material.FlowingFluid;
import net.minecraft.world.level.material.Fluid;
import net.minecraft.world.level.pathfinder.BlockPathTypes;
import net.minecraftforge.common.SoundActions;
import net.minecraftforge.fluids.FluidType;
import net.minecraftforge.fluids.ForgeFlowingFluid;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

public class TFCMFluids {
    public static final DeferredRegister<FluidType> FLUID_TYPES = DeferredRegister.create(ForgeRegistries.Keys.FLUID_TYPES, TFCMineralogy.MODID);
    public static final DeferredRegister<Fluid> FLUIDS = DeferredRegister.create(Registries.FLUID, TFCMineralogy.MODID);

    public static final int ALPHA_MASK = 0xFF000000;
    public static final ResourceLocation MOLTEN_STILL = Helpers.identifier("block/molten_still");
    public static final ResourceLocation MOLTEN_FLOW = Helpers.identifier("block/molten_flow");
    public static final ResourceLocation WATER_STILL = Helpers.identifierMC("block/water_still");
    public static final ResourceLocation WATER_FLOW = Helpers.identifierMC("block/water_flow");
    public static final ResourceLocation WATER_OVERLAY = Helpers.identifierMC("block/water_overlay");
    /** @see net.minecraft.client.renderer.ScreenEffectRenderer#UNDERWATER_LOCATION */
    public static final ResourceLocation UNDERWATER_LOCATION = Helpers.identifierMC("textures/misc/underwater.png");

    // Register Molten Metals - if they're supposed to have an unique fluid (hasLiquidState)
    public static final Map<TFCMMetal.Default, FluidRegistryObject<ForgeFlowingFluid>> METALS = Helpers.mapOfKeys(TFCMMetal.Default.class, TFCMMetal.Default::hasLiquidState, metal -> register(
        "metal/" + metal.getSerializedName(),
        properties -> properties
            .block(TFCMBlocks.METAL_FLUIDS.get(metal))
            .bucket(TFCMItems.FLUID_BUCKETS.get(TFCMFluidId.asType(metal)))
            .explosionResistance(100),
        lavaLike()
            .descriptionId("fluid.tfcm.metal." + metal.getSerializedName())
            .rarity(metal.getRarity()),
        new FluidTypeClientProperties(ALPHA_MASK | metal.getColor(), MOLTEN_STILL, MOLTEN_FLOW, null, null),
        MoltenFluid.Source::new,
        MoltenFluid.Flowing::new
    ));
    // Register Simple Fluids
    public static final Map<TFCMSimpleFluid, FluidRegistryObject<ForgeFlowingFluid>> SIMPLE_FLUIDS = Helpers.mapOfKeys(TFCMSimpleFluid.class, fluid -> register(
        fluid.getId(),
        properties -> properties
            .block(TFCMBlocks.SIMPLE_FLUIDS.get(fluid))
            .bucket(TFCMItems.FLUID_BUCKETS.get(TFCMFluidId.asType(fluid))),
        waterLike()
            .descriptionId("fluid.tfcm." + fluid.getId())
            .canConvertToSource(false),
        new FluidTypeClientProperties(fluid.isTransparent() ? ALPHA_MASK | fluid.getColor() : fluid.getColor(), WATER_STILL, WATER_FLOW, WATER_OVERLAY, UNDERWATER_LOCATION),
        MixingFluid.Source::new,
        MixingFluid.Flowing::new
    ));

    private static FluidType.Properties lavaLike()
    {
        return FluidType.Properties.create()
            .adjacentPathType(BlockPathTypes.LAVA)
            .sound(SoundActions.BUCKET_FILL, SoundEvents.BUCKET_FILL)
            .sound(SoundActions.BUCKET_EMPTY, SoundEvents.BUCKET_EMPTY_LAVA)
            .lightLevel(15)
            .density(3000)
            .viscosity(6000)
            .temperature(1300)
            .canConvertToSource(false)
            .canDrown(false)
            .canExtinguish(false)
            .canHydrate(false)
            .canPushEntity(false)
            .canSwim(false)
            .supportsBoating(false);
    }

    private static FluidType.Properties waterLike()
    {
        return FluidType.Properties.create()
            .adjacentPathType(BlockPathTypes.WATER)
            .sound(SoundActions.BUCKET_FILL, SoundEvents.BUCKET_FILL)
            .sound(SoundActions.BUCKET_EMPTY, SoundEvents.BUCKET_EMPTY)
            .canConvertToSource(true)
            .canDrown(true)
            .canExtinguish(true)
            .canHydrate(true)
            .canPushEntity(true)
            .canSwim(true)
            .supportsBoating(true);
    }
    private static <F extends FlowingFluid> FluidRegistryObject<F> register(String name, Consumer<ForgeFlowingFluid.Properties> builder, FluidType.Properties typeProperties, FluidTypeClientProperties clientProperties, Function<ForgeFlowingFluid.Properties, F> sourceFactory, Function<ForgeFlowingFluid.Properties, F> flowingFactory)
    {
        // Names `metal/foo` to `metal/flowing_foo`
        final int index = name.lastIndexOf('/');
        final String flowingName = index == -1 ? "flowing_" + name : name.substring(0, index) + "/flowing_" + name.substring(index + 1);

        return RegistrationHelpers.registerFluid(FLUID_TYPES, FLUIDS, name, name, flowingName, builder, () -> new ExtendedFluidType(typeProperties, clientProperties), sourceFactory, flowingFactory);
    }
}
