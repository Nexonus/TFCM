package dev.nexreon.tfcm.client;

import dev.nexreon.tfcm.common.blocks.TFCMBlocks;
import dev.nexreon.tfcm.common.items.TFCMItems;
import dev.nexreon.tfcm.util.TFCMMetal;
import net.dries007.tfc.common.items.TFCFishingRodItem;
import net.dries007.tfc.util.Helpers;
import net.minecraft.client.renderer.ItemBlockRenderTypes;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

public class TFCMClientEvenHandler {

    public static void init()
    {
        @SuppressWarnings("removal")
        final IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();

        bus.addListener(TFCMClientEvenHandler::clientSetup); // Our clientSetup
    }
    @SuppressWarnings("removal")
    public static void clientSetup(FMLClientSetupEvent event)
    {
        event.enqueueWork(() -> {
            for (TFCMMetal.Default metal : TFCMMetal.Default.values())
            {
                if (metal.hasTools())
                {
                    
                    Item rod = TFCMItems.METAL_ITEMS.get(metal).get(TFCMMetal.ItemType.FISHING_ROD).get();
                    ItemProperties.register(rod, Helpers.identifier("cast"), (stack, level, entity, unused) -> {
                        if (entity == null)
                        {
                            return 0.0F;
                        }
                        else
                        {
                            return entity instanceof Player player && TFCFishingRodItem.isThisTheHeldRod(player, stack) && player.fishing != null ? 1.0F : 0.0F;
                        }
                    });
                    

                    Item shield = TFCMItems.METAL_ITEMS.get(metal).get(TFCMMetal.ItemType.SHIELD).get();
                    ItemProperties.register(shield, Helpers.identifierMC("blocking"), (stack, level, entity, unused) -> {
                        if (entity == null)
                        {
                            return 0.0F;
                        }
                        else
                        {
                            return entity instanceof Player && entity.isUsingItem() && entity.getUseItem() == stack ? 1.0f : 0.0f;
                        }
                    });

                    Item javelin = TFCMItems.METAL_ITEMS.get(metal).get(TFCMMetal.ItemType.JAVELIN).get();
                    ItemProperties.register(javelin, Helpers.identifier("throwing"), (stack, level, entity, unused) ->
                        entity != null && ((entity.isUsingItem() && entity.getUseItem() == stack) || (entity instanceof Monster monster && monster.isAggressive())) ? 1.0F : 0.0F
                    );
                }
            }
        });
        //final RenderType solid = RenderType.solid();
        final RenderType cutout = RenderType.cutout();
        //final RenderType cutoutMipped = RenderType.cutoutMipped();
        //final RenderType translucent = RenderType.translucent();
        //final Predicate<RenderType> ghostBlock = rt -> rt == cutoutMipped || rt == Sheets.translucentCullBlockSheet();

        TFCMBlocks.ORES.values().forEach(map -> map.values().forEach(reg -> ItemBlockRenderTypes.setRenderLayer(reg.get(), cutout)));
        TFCMBlocks.GRADED_ORES.values().forEach(map -> map.values().forEach(inner -> inner.values().forEach(reg -> ItemBlockRenderTypes.setRenderLayer(reg.get(), cutout))));

        TFCMBlocks.METALS.values().forEach(map -> map.values().forEach(reg -> ItemBlockRenderTypes.setRenderLayer(reg.get(), cutout)));

    };
}
