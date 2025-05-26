package dev.nexreon.tfcmineralogy;

import net.minecraftforge.fml.common.Mod;
import dev.nexreon.tfcmineralogy.init.CreativeTabInit;
import dev.nexreon.tfcmineralogy.init.BlockInit;
import dev.nexreon.tfcmineralogy.init.ItemInit;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(TFCMineralogy.MODID)
public class TFCMineralogy{
    public static final String MODID = "tfcmineralogy";

    public TFCMineralogy(){
        IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();
        BlockInit.BLOCKS.register(bus);
        ItemInit.ITEMS.register(bus);
        CreativeTabInit.TABS.register(bus);
    }
}