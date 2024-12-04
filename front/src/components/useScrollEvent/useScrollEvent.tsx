import { useEffect } from "react";

export const useScrollEvent = (listener: (this: Window, ev: Event) => any) => {
  useEffect(() => {
    window.addEventListener("scroll", listener);

    return () => {
      window.removeEventListener("scroll", listener);
    };
  }, []);
};
