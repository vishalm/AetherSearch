import SvgAetherSearchLogo from "@opal/logos/aethersearch-logo";
import SvgAetherSearchTyped from "@opal/logos/aethersearch-typed";
import { cn } from "@opal/utils";

interface AetherSearchLogoTypedProps {
  size?: number;
  className?: string;
}

// # NOTE(@raunakab):
// This ratio is not some random, magical number; it is available on Figma.
const HEIGHT_TO_GAP_RATIO = 5 / 16;

const SvgAetherSearchLogoTyped = ({ size: height, className }: AetherSearchLogoTypedProps) => {
  const gap = height != null ? height * HEIGHT_TO_GAP_RATIO : undefined;

  return (
    <div
      className={cn(`flex flex-row items-center`, className)}
      style={{ gap }}
    >
      <SvgAetherSearchLogo size={height} />
      <SvgAetherSearchTyped size={height} />
    </div>
  );
};
export default SvgAetherSearchLogoTyped;
