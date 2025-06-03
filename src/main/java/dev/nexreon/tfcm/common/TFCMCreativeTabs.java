package dev.nexreon.tfcm.common;

import dev.nexreon.tfcm.TFCMineralogy;
import dev.nexreon.tfcm.common.blocks.TFCMBlocks;
import dev.nexreon.tfcm.common.blocks.rock.TFCMOre;
import dev.nexreon.tfcm.common.items.TFCMItems;
import dev.nexreon.tfcm.util.TFCMMetal;

import java.util.Map;
import java.util.function.Supplier;
import java.util.stream.Stream;

import net.dries007.tfc.TerraFirmaCraft;
import net.dries007.tfc.util.SelfTests;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.ItemLike;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

public class TFCMCreativeTabs {
    public static final DeferredRegister<CreativeModeTab> CREATIVE_TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, TFCMineralogy.MODID);
    public static final CreativeTabHolder TFCM_ORES = register("tfcm_ores", () -> new ItemStack(TFCMItems.GRADED_ORES.get(TFCMOre.SMITHSONITE).get(TFCMOre.Grade.NORMAL).get()), TFCMCreativeTabs::fillOresTab);
    public static final CreativeTabHolder TFCM_MISC = register("tfcm_misc", () -> new ItemStack(TFCMItems.ORE_POWDERS.get(TFCMOre.GALENA).get()), TFCMCreativeTabs::fillMiscTab);
    public static final CreativeTabHolder TFCM_METAL = register("tfcm_metals", () -> new ItemStack(TFCMItems.METAL_ITEMS.get(TFCMMetal.Default.LEAD).get(TFCMMetal.ItemType.INGOT).get()), TFCMCreativeTabs::fillMetalTab);
    public static Stream<CreativeModeTab.DisplayItemsGenerator> generators()
    {
        return Stream.of(TFCM_ORES).map(holder -> holder.generator);
    }

    // Fill Ores Tab
    private static void fillOresTab(CreativeModeTab.ItemDisplayParameters parameters, CreativeModeTab.Output out)
    {
        for (TFCMOre ore : TFCMOre.values())
        {
            if (ore.isGraded())
            {
                accept(out, TFCMItems.GRADED_ORES, ore, TFCMOre.Grade.POOR);
                //accept(out, TFCMBlocks.SMALL_ORES, ore); // Not available right now
                accept(out, TFCMItems.GRADED_ORES, ore, TFCMOre.Grade.NORMAL);
                accept(out, TFCMItems.GRADED_ORES, ore, TFCMOre.Grade.RICH);
            }
        }
        for (TFCMOre ore : TFCMOre.values())
        {
            if (!ore.isGraded())
            {
                accept(out, TFCMItems.ORES, ore);
            }
        }
        /* 
        for (Gem gem : Gem.values())
        {
            accept(out, TFCItems.GEMS, gem);
            accept(out, TFCItems.GEM_DUST, gem);
        }
        for (OreDeposit deposit : OreDeposit.values())
        {
            TFCBlocks.ORE_DEPOSITS.values().forEach(map -> accept(out, map, deposit));
        }
        */ // Not available right now
        for (TFCMOre ore : TFCMOre.values())
        {
            if (ore.isGraded())
            {
                TFCMBlocks.GRADED_ORES.values().forEach(map -> map.get(ore).values().forEach(reg -> accept(out, reg)));
            }
            else
            {
                TFCMBlocks.ORES.values().forEach(map -> accept(out, map, ore));
            }
        }
    }
    // Fill Misc Tab
    private static void fillMiscTab(CreativeModeTab.ItemDisplayParameters parameters, CreativeModeTab.Output out)
    {
        TFCMItems.ORE_POWDERS.values().forEach(p -> accept(out, p));
    }
    // Helpers for registration
    private static CreativeTabHolder register(String name, Supplier<ItemStack> icon, CreativeModeTab.DisplayItemsGenerator displayItems)
    {
        final RegistryObject<CreativeModeTab> reg = CREATIVE_TABS.register(name, () -> CreativeModeTab.builder()
            .icon(icon)
            .title(Component.translatable("tfcm.creative_tab." + name))
            .displayItems(displayItems)
            .build());
        return new CreativeTabHolder(reg, displayItems);
    }
    // Fill Metal Tab
    private static void fillMetalTab(CreativeModeTab.ItemDisplayParameters parameters, CreativeModeTab.Output out)
    {
        for (TFCMMetal.Default metal : TFCMMetal.Default.values())
        {
            for (TFCMMetal.BlockType type : new TFCMMetal.BlockType[] {
                TFCMMetal.BlockType.ANVIL,
                TFCMMetal.BlockType.BLOCK,
                TFCMMetal.BlockType.BLOCK_SLAB,
                TFCMMetal.BlockType.BLOCK_STAIRS,
                TFCMMetal.BlockType.BARS,
                TFCMMetal.BlockType.CHAIN,
                TFCMMetal.BlockType.TRAPDOOR,
                TFCMMetal.BlockType.LAMP,
            })
            {
                accept(out, TFCMBlocks.METALS, metal, type);
            }

            accept(out, TFCMItems.METAL_ITEMS, metal, TFCMMetal.ItemType.UNFINISHED_LAMP);

            if (metal == TFCMMetal.Default.LEAD)
            {
                accept(out, TFCMBlocks.LEAD_PIPE);
            }

            for (TFCMMetal.ItemType itemType : new TFCMMetal.ItemType[] {
                TFCMMetal.ItemType.INGOT,
                TFCMMetal.ItemType.DOUBLE_INGOT,
                TFCMMetal.ItemType.SHEET,
                TFCMMetal.ItemType.DOUBLE_SHEET,
                TFCMMetal.ItemType.ROD,

                TFCMMetal.ItemType.TUYERE,

                TFCMMetal.ItemType.PICKAXE,
                TFCMMetal.ItemType.PROPICK,
                TFCMMetal.ItemType.AXE,
                TFCMMetal.ItemType.SHOVEL,
                TFCMMetal.ItemType.HOE,
                TFCMMetal.ItemType.CHISEL,
                TFCMMetal.ItemType.HAMMER,
                TFCMMetal.ItemType.SAW,
                TFCMMetal.ItemType.KNIFE,
                TFCMMetal.ItemType.SCYTHE,
                TFCMMetal.ItemType.JAVELIN,
                TFCMMetal.ItemType.SWORD,
                TFCMMetal.ItemType.MACE,
                TFCMMetal.ItemType.FISHING_ROD,
                TFCMMetal.ItemType.SHEARS,

                TFCMMetal.ItemType.HELMET,
                TFCMMetal.ItemType.CHESTPLATE,
                TFCMMetal.ItemType.GREAVES,
                TFCMMetal.ItemType.BOOTS,

                TFCMMetal.ItemType.SHIELD,
                TFCMMetal.ItemType.HORSE_ARMOR,

                TFCMMetal.ItemType.PICKAXE_HEAD,
                TFCMMetal.ItemType.PROPICK_HEAD,
                TFCMMetal.ItemType.AXE_HEAD,
                TFCMMetal.ItemType.SHOVEL_HEAD,
                TFCMMetal.ItemType.HOE_HEAD,
                TFCMMetal.ItemType.CHISEL_HEAD,
                TFCMMetal.ItemType.HAMMER_HEAD,
                TFCMMetal.ItemType.SAW_BLADE,
                TFCMMetal.ItemType.KNIFE_BLADE,
                TFCMMetal.ItemType.SCYTHE_BLADE,
                TFCMMetal.ItemType.JAVELIN_HEAD,
                TFCMMetal.ItemType.SWORD_BLADE,
                TFCMMetal.ItemType.MACE_HEAD,
                TFCMMetal.ItemType.FISH_HOOK,

                TFCMMetal.ItemType.UNFINISHED_HELMET,
                TFCMMetal.ItemType.UNFINISHED_CHESTPLATE,
                TFCMMetal.ItemType.UNFINISHED_GREAVES,
                TFCMMetal.ItemType.UNFINISHED_BOOTS,
            })
            {
                accept(out, TFCMItems.METAL_ITEMS, metal, itemType);
            }
        }
    }

    private static <T extends ItemLike, R extends Supplier<T>, K1, K2> void accept(CreativeModeTab.Output out, Map<K1, Map<K2, R>> map, K1 key1, K2 key2)
    {
        if (map.containsKey(key1) && map.get(key1).containsKey(key2))
        {
            out.accept(map.get(key1).get(key2).get());
        }
    }

    private static <T extends ItemLike, R extends Supplier<T>, K> void accept(CreativeModeTab.Output out, Map<K, R> map, K key)
    {
        if (map.containsKey(key))
        {
            out.accept(map.get(key).get());
        }
    }

    private static <T extends ItemLike, R extends Supplier<T>> void accept(CreativeModeTab.Output out, R reg)
    {
        if (reg.get().asItem() == Items.AIR)
        {
            TerraFirmaCraft.LOGGER.error("BlockItem with no Item added to creative tab: " + reg);
            SelfTests.reportExternalError();
            return;
        }
        out.accept(reg.get());
    }
    public record CreativeTabHolder(RegistryObject<CreativeModeTab> tab, CreativeModeTab.DisplayItemsGenerator generator) {}
}
