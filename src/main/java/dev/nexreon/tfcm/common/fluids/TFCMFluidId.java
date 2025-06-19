package dev.nexreon.tfcm.common.fluids;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.OptionalInt;
import java.util.function.Function;
import java.util.function.Supplier;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import dev.nexreon.tfcm.util.TFCMMetal;
import net.minecraft.world.level.material.Fluid;

public record TFCMFluidId(String name, OptionalInt color, Supplier<? extends Fluid> fluid)
{
    private static final Map<Enum<?>, TFCMFluidId> IDENTITY = new HashMap<>();
    private static final List<TFCMFluidId> VALUES = Stream.of(
            Arrays.stream(TFCMSimpleFluid.values()).map(fluid -> fromEnum(fluid, fluid.getColor(), fluid.getId(), TFCMFluids.SIMPLE_FLUIDS.get(fluid).source())),
            Arrays.stream(TFCMMetal.Default.values()).filter(metal -> metal.hasLiquidState()).map(metal -> fromEnum(metal, metal.getColor(), "metal/" + metal.getSerializedName(), TFCMFluids.METALS.get(metal).source()))
        )
        .flatMap(Function.identity())
        .toList();

    public static <R> Map<TFCMFluidId, R> mapOf(Function<? super TFCMFluidId, ? extends R> map)
    {
        return VALUES.stream().collect(Collectors.toMap(Function.identity(), map));
    }

    public static TFCMFluidId asType(Enum<?> identity)
    {
        return IDENTITY.get(identity);
    }

    private static TFCMFluidId fromEnum(Enum<?> identity, int color, String name, Supplier<? extends Fluid> fluid)
    {
        final TFCMFluidId type = new TFCMFluidId(name, OptionalInt.of(TFCMFluids.ALPHA_MASK | color), fluid);
        IDENTITY.put(identity, type);
        return type;
    }
}