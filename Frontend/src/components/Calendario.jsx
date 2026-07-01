import { useEffect, useRef } from "react";
import flatpickr from "flatpickr";
import { Portuguese } from "flatpickr/dist/l10n/pt";
import "flatpickr/dist/flatpickr.min.css";

export default function Calendario({ onPeriodoChange }) {
  const inputRef = useRef(null);

useEffect(() => {
  const calendario = flatpickr(inputRef.current, {
    locale: Portuguese,
    mode: "range",
    dateFormat: "d-m-Y",

    onChange(selectedDates) {
      if (selectedDates.length === 2) {
        const inicio = transformarData(selectedDates[0]);
        const fim = transformarData(selectedDates[1]);

        onPeriodoChange(inicio, fim);
      }
    },
  });

  return () => calendario.destroy();
}, [onPeriodoChange]);

  function transformarData(data) {
    const ano = data.getFullYear();
    const mes = String(data.getMonth() + 1).padStart(2, "0");
    const dia = String(data.getDate()).padStart(2, "0");

    return `${ano}-${mes}-${dia}`;
  }

  return (
    <input
      ref={inputRef}
      id="periodo"
      placeholder="Período"
      readOnly
    />
  );
}