package dev.nexreon.tfcm.common.fluids;

import java.util.Locale;

public enum TFCMSimpleFluid {
    AMMONIZED_WATER(0xFFA7C8DD);

    private final String id;
    private final int color;

    TFCMSimpleFluid(int color)
    {
        this.id = name().toLowerCase(Locale.ROOT);
        this.color = color;
    }

    public String getId()
    {
        return id;
    }

    public int getColor()
    {
        return color;
    }

    public boolean isTransparent()
    {
        return true; // Temporary, change when adding non-transparent fluids
        //return this != CURDLED_MILK && this != MILK_VINEGAR;
    }
}
