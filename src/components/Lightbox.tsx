import { Dialog, DialogContent, DialogTitle } from "@/components/ui/dialog";

interface Props {
  src: string | null;
  caption: string;
  onClose: () => void;
}

export function Lightbox({ src, caption, onClose }: Props) {
  return (
    <Dialog open={!!src} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-[95vw] border-gold/30 bg-background p-3 sm:max-w-xl">
        <DialogTitle className="font-display text-sm tracking-wide">{caption}</DialogTitle>
        {src && (
          <img src={src} alt={caption} className="max-h-[75vh] w-full rounded-sm object-contain" />
        )}
      </DialogContent>
    </Dialog>
  );
}
