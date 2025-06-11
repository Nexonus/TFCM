package dev.nexreon.tfcm.common.blocks.rock;

import net.dries007.tfc.util.registry.RegistryRock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;

public enum TFCMOre
{
    SMITHSONITE(true),
    GALENA(true),
    ORPIMENT(false),
    REALGAR(false),
    VIVIANITE(false),
    ARSENOPYRITE(true),
    SALMIAC(false);

    private final boolean graded;

    TFCMOre(boolean graded)
    {
        this.graded = graded;
    }

    public boolean isGraded()
    {
        return graded;
    }

    public Block create(RegistryRock rock)
    {
        // Same hardness as raw rock
        final BlockBehaviour.Properties properties = Block.Properties.of().mapColor(MapColor.STONE).sound(SoundType.STONE).strength(rock.category().hardness(6.5f), 10).requiresCorrectToolForDrops();
        /* 
        if (this == LIGNITE || this == BITUMINOUS_COAL)
        {
            return new ExtendedBlock(ExtendedProperties.of(properties).flammable(5, 120));
        }*/ // Use only for flammables 
        return new Block(properties);
    }

    public enum Grade
    {
        POOR, NORMAL, RICH;

        private static final Grade[] VALUES = values();

        public static Grade valueOf(int i)
        {
            return i < 0 || i >= VALUES.length ? NORMAL : VALUES[i];
        }
    }
}