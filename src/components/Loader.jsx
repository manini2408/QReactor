import { motion } from 'framer-motion';

const Loader = () => {
  return (
    <div className="loader-container">
      <motion.div 
        className="loader"
        animate={{ 
          rotate: 360,
          scale: [1, 1.2, 1],
        }}
        transition={{ 
          duration: 1.5, 
          repeat: Infinity,
          ease: "easeInOut" 
        }}
      >
        <div className="loader-circle"></div>
      </motion.div>
    </div>
  );
};

export default Loader; 