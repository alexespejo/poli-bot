import { useState, useEffect } from "react";
import { motion, useAnimation } from "framer-motion";

const TypingAnimation = ({ text, delay }) => {
 const [isVisible, setIsVisible] = useState(false);
 const controls = useAnimation();

 useEffect(() => {
  const timeout = setTimeout(() => {
   setIsVisible(true);
   controls.start({
    opacity: [0, 1],
    transition: { duration: 0.1 },
   });
  }, delay);

  return () => clearTimeout(timeout);
 }, [controls, delay]);

 return (
  <motion.div
   initial={{ opacity: 0 }}
   animate={isVisible ? "visible" : "hidden"}
   variants={{
    visible: { opacity: 1 },
    hidden: { opacity: 0 },
   }}
  >
   {text.split("").map((char, index) => (
    <motion.span
     key={index}
     style={{ display: "inline-block" }}
     initial={{ opacity: 0 }}
     animate={{ opacity: 1 }}
     transition={{ delay: index * 0.01 }}
    >
     {char}
    </motion.span>
   ))}
  </motion.div>
 );
};

export default TypingAnimation;
