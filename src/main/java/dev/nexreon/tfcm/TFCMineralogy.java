package dev.nexreon.tfcm;

import net.minecraftforge.fml.common.Mod;
import dev.nexreon.tfcm.client.TFCMSounds;
import dev.nexreon.tfcm.common.TFCMCreativeTabs;
import dev.nexreon.tfcm.common.blocks.TFCMBlocks;
import dev.nexreon.tfcm.common.fluids.TFCMFluids;
import dev.nexreon.tfcm.common.items.TFCMItems;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(TFCMineralogy.MODID)
public class TFCMineralogy{
    
    public static final String MODID = "tfcmineralogy";

    public TFCMineralogy(){
        @SuppressWarnings("removal")
        IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();

        TFCMBlocks.BLOCKS.register(bus);
        TFCMItems.ITEMS.register(bus);
        TFCMCreativeTabs.CREATIVE_TABS.register(bus);
        TFCMFluids.FLUID_TYPES.register(bus);
        TFCMFluids.FLUIDS.register(bus);
        TFCMSounds.SOUNDS.register(bus);
        /* 
        BlockInit.BLOCKS.register(bus);
        ItemInit.ITEMS.register(bus);
        CreativeTabInit.TABS.register(bus);
        FluidInit.FLUIDS.register(bus);
        */
    }
}
