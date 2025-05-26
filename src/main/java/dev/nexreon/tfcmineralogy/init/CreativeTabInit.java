package dev.nexreon.tfcmineralogy.init;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;

import com.google.common.eventbus.Subscribe;

import dev.nexreon.tfcmineralogy.TFCMineralogy;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.ItemLike;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;


@Mod.EventBusSubscriber(modid = TFCMineralogy.MODID, bus=Mod.EventBusSubscriber.Bus.MOD)
public class CreativeTabInit {
    public static final DeferredRegister<CreativeModeTab>TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, TFCMineralogy.MODID);

    public static final List<Supplier<? extends ItemLike>> TFCMINERALOGY_LIST = new ArrayList<>();

    public static final RegistryObject<CreativeModeTab>TFCMINERALOGY_TAB = TABS.register("tfcmineralogy_tab",
    () -> CreativeModeTab.builder()
    .title(Component.translatable("itemGroup.tfcmineralogy_tab"))
    .icon(() -> ItemInit.EXAMPLE_ITEM.get().getDefaultInstance())
    .displayItems((displayParams, output) -> {
        TFCMINERALOGY_LIST.forEach(itemLike -> output.accept(itemLike.get()));
    })
    .build()
    );

    public static <T extends Item> RegistryObject<T> addToTab(RegistryObject<T>itemLike){
        TFCMINERALOGY_LIST.add(itemLike);
        return itemLike;
    }
    @SubscribeEvent
    public static void buildContents(BuildCreativeModeTabContentsEvent event){
        // Add items to other tabs if needed here.
    }
}
