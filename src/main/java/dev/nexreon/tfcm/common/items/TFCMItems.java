package dev.nexreon.tfcm.common.items;

import java.util.Locale;
import java.util.Map;
import java.util.function.Supplier;

import dev.nexreon.tfcm.TFCMineralogy;
import dev.nexreon.tfcm.common.blocks.rock.TFCMOre;
import dev.nexreon.tfcm.common.fluids.TFCMFluidId;
import dev.nexreon.tfcm.util.TFCMMetal;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.BucketItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;
import net.dries007.tfc.util.Helpers;

public final class TFCMItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(Registries.ITEM, TFCMineralogy.MODID);
    
    // Ores Registry
    public static final Map<TFCMOre, RegistryObject<Item>> ORES = Helpers.mapOfKeys(TFCMOre.class, ore -> !ore.isGraded(), type ->
    register("ore/" + type.name()));
    // Graded Ores
    public static final Map<TFCMOre, Map<TFCMOre.Grade, RegistryObject<Item>>> GRADED_ORES = Helpers.mapOfKeys(TFCMOre.class, TFCMOre::isGraded, ore ->
        Helpers.mapOfKeys(TFCMOre.Grade.class, grade ->
            register("ore/" + grade.name() + '_' + ore.name())
        )
    );
    // Fluid Buckets
    public static final Map<TFCMFluidId, RegistryObject<BucketItem>> FLUID_BUCKETS = TFCMFluidId.mapOf(fluid ->
        register("bucket/" + fluid.name(), () -> new BucketItem(fluid.fluid(), new Item.Properties().craftRemainder(Items.BUCKET).stacksTo(1)))
    );

    // Metal Items
    public static final Map<TFCMMetal.Default, Map<TFCMMetal.ItemType, RegistryObject<Item>>> METAL_ITEMS = Helpers.mapOfKeys(TFCMMetal.Default.class, metal ->
        Helpers.mapOfKeys(TFCMMetal.ItemType.class, type -> type.has(metal), type -> // Figure out how to get rid of ingot
            register("metal/" + type.name() + "/" + metal.name(), () -> type.create(metal))
        )
    );

    public static final Map<TFCMOre, RegistryObject<Item>> ORE_POWDERS = Helpers.mapOfKeys(TFCMOre.class, ore -> register("powder/" + ore.name())); // TFCMOre::isGraded optional
    /* // Use this to add gems to TFCM
    public static final Map<Gem, RegistryObject<Item>> GEMS = Helpers.mapOfKeys(Gem.class, gem ->
        register("gem/" + gem.name())
    );
    public static final Map<Gem, RegistryObject<Item>> GEM_DUST = Helpers.mapOfKeys(Gem.class, gem -> register("powder/" + gem.name()));
    */

    // Private classes for registration
    private static RegistryObject<Item> register(String name)
    {
        return register(name, () -> new Item(new Item.Properties()));
    }

    private static <T extends Item> RegistryObject<T> register(String name, Supplier<T> item)
    {
        return ITEMS.register(name.toLowerCase(Locale.ROOT), item);
    }
}
